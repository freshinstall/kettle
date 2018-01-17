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
# repos.py - Repository module for Kettle

import shutil, subprocess, os
from softwareproperties.SoftwareProperties import SoftwareProperties

from . import module

import gettext
_ = gettext.gettext

class BadKettle(Exception):
    pass

class Repos(module.Module):

    sp = SoftwareProperties()
    ppas_list = []
    module_path = os.path.dirname(os.path.realpath(__file__))

    def get_ppas(self):
        try:
            ppas_member = self.kettle_ark.getmember('data/repos/ppas.repos')
        except KeyError:
            raise BadKettle(_("The kettle is missing data for module: repos"))

        ppas_exfile = self.kettle_ark.extractfile(ppas_member)
        ppas_bytes = ppas_exfile.readlines()
        ppas_exfile.close()


        for i in ppas_bytes:
            line = i.decode('UTF-8')[:-1]
            self.ppas_list.append(line)
        return self.ppas_list


    def install_repos(self, repo_list):
        for i in repo_list:
            try:
                self.sp.add_source_from_line(i)
                self.sp.sourceslist.save()
                self.sp.reload_sourceslist()
            except:
                raise BadRepo(_("Couldn't add the repository %s" % i))

    def get_to_root(self):
        subprocess.call(["/usr/bin/sudo",
                         "/usr/bin/python3",
                         self.module_path + "/repos-data/as_root.py",
                         self.kettle.path])

    def run_install(self):
        self.get_to_root()
        
