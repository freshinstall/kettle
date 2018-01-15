#!/usr/bin/python3

## kettle - Desktop software configuration manager
# Copyright (c) 2018, freshinstall
# All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED “AS IS” AND ISC DISCLAIMS ALL WARRANTIES WITH REGARD 
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL ISC BE LIABLE FOR  ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
#
# ket.py - Kettle object class

import tarfile
import yaml
import gettext
_ = gettext.gettext

class BadKettle(Exception):
    pass

class Kettle():
    name = ""
    ketid = ""
    modules = []
    permissions = []
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
        self.get_id()

        self.tmppath = "/tmp/kettle/%s" % self.ketid

    def get_id(self):
        self.ketid = self.kettle_yaml['id']
        return self.ketid

    def get_yaml(self):

        try:
            kettle_yaml_info = self.kettle_ark.getmember('metainfo/meta.yaml')
        except KeyError:
            raise BadKettle(_("The kettle is missing meta.yaml"))

        kettle_yaml_b = self.kettle_ark.extractfile(kettle_yaml_info)
        self.kettle_yaml = yaml.safe_load(kettle_yaml_b)

        return self.kettle_yaml

    def get_modules(self):
        self.log.debug(_('this is only here for imports'))
        self.modules = self.kettle_yaml['modules']
        return self.modules

    def extract_kettle(self, path=tmppath):
        self.kettle_ark.extractall(path=path)

