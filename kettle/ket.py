#!/usr/bin/python3

## kettle - Desktop software configuration manager
# Copyright (c) 2018, Ian Santopietro <isantop@gmail.com>
# All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR  ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
# ket.py - Kettle object class

import tarfile
import yaml
import glob, os
import logging

import gettext
_ = gettext.gettext

class BadKettle(Exception):
    pass

class Kettle():
    name = ""
    ketid = ""
    modules = []
    permissions = {}
    standard = 0
    tmppath = "/tmp/kettle/"
    kettle_yaml = []

    def __init__(self, path):
        self.path = path

        try:
            self.kettle_ark = tarfile.open(name=self.path, mode='r')
        except FileNotFoundError:
            raise BadKettle(_('The kettle doesn\'t exist'))

        self.get_yaml()
        self.get_name()
        self.get_id()
        self.get_modules()
        self.get_permissions()

        self.tmppath = "/tmp/kettle/%s" % self.ketid

    def get_yaml(self):
        try:
            kettle_yaml_info = self.kettle_ark.getmember('metainfo/meta.yaml')
        except KeyError:
            raise BadKettle(_("The kettle is missing meta.yaml"))

        kettle_yaml_b = self.kettle_ark.extractfile(kettle_yaml_info)
        self.kettle_yaml = yaml.safe_load(kettle_yaml_b)

        return self.kettle_yaml

    def get_name(self):
        self.name = self.kettle_yaml['name']
        return self.name

    def get_id(self):
        self.ketid = self.kettle_yaml['id']
        return self.ketid

    def get_modules(self):
        self.modules = self.kettle_yaml['modules']
        return self.modules

    def get_permissions(self):
        self.permissions = self.kettle_yaml['permissions']
        return self.permissions

    def extract_kettle(self, path=tmppath):
        self.kettle_ark.extractall(path=path)

class NewKettle(Kettle):

    name = ""
    ketid = ""
    modules = []
    permissions = {}
    standard = 0
    tmppath = "/tmp/kettle/"
    kettle_yaml = []

    def __init__(self, path):
        self.log = logging.getLogger('kettle.NewKettle')
        self.log.debug(_("Logging set up!"))
        self.path = path
        with open(os.path.join(self.path, "metainfo/meta.yaml")) as f:
            self.kettle_yaml = yaml.safe_load(f)

        self.ketid = self.kettle_yaml['id']
        kettle_filename = ("%s.ket" % self.ketid)

        try:
            self.kettle_ark = tarfile.open(name=kettle_filename, mode='x')
        except FileExistsError:
            raise BadKettle(_('That kettle already exists!'))

    def create(self):
        self.log.info(_("Adding %s to kettle" % self.path))
        os.chdir(self.path)
        self.kettle_ark.add("data")
        self.kettle_ark.add("metainfo")

    def close(self):
        self.kettle_ark.close()
