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
        self.kettle_ark = tarfile.open(name=self.path, mode='r')
        try:
            kettle_yaml_info = self.kettle_ark.getmember('metainfo/meta.yaml')
        except KeyError:
            raise BadKettle("The kettle is missing meta.yaml")
        kettle_yaml_b = self.kettle_ark.extractfile(kettle_yaml_info)
        for i in kettle_yaml_b.readlines():
            self.kettle_yaml.append(str(i)[2:-3])
        for i in self.kettle_yaml:
            if i.startswith("id: "):
                self.ketid = i[4:]
        self.tmppath = "/tmp/kettle/%s" % self.ketid

    def get_yaml(self):
        return self.kettle_yaml

    def get_id(self):
        return self.ketid

    def extract_kettle(self, path=tmppath):
        self.kettle_ark.extractall(path=path)
