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
# packages.py - Kettle apt packages module

import apt
import sys, os
import subprocess
import logging

from . import plugin

import gettext
_ = gettext.gettext

class BadKettle(Exception):
    pass

class Packages(plugin.Plugin):

    permissions = {'script': False,
                   'root': True,
                   'remove-pkg': True,
                   'system-config': True
                   }
    cache = apt.cache.Cache()
    package_install = []
    package_remove = []

    def __init__(self, kettle):
        super().__init__(kettle)
        self.log = logging.getLogger('kettle.Plugin.Packages')
        self.log.debug(_("Logging set up!"))
        self.permissions = self.kettle.permissions

        try:
            package_install_info = self.kettle_ark.getmember('data/packages/install.deblist')
            package_remove_info = self.kettle_ark.getmember('data/packages/remove.deblist')
        except KeyError:
            raise BadKettle(_('The kettle is missing data for module: Packages'))

        package_install_b = self.kettle_ark.extractfile(package_install_info)
        package_remove_b = self.kettle_ark.extractfile(package_remove_info)
        self.remove_allowed = self.permissions['remove-pkg']

        for i in package_install_b:
            if not str(i).startswith("b'#"):
                self.package_install.append(str(i)[2:-3])

        if self.remove_allowed:
            for i in package_remove_b:
                if not str(i).startswith("b'#"):
                    self.package_remove.append(str(i)[2:-3])

    def cache_lock(self):
        self.cache.update()
        self.cache.open()

    def cache_unlock(self):
        self.cache.close()

    def mark_pkg_install(self, package):
        try:
            pkg = self.cache[package]
            if pkg.is_installed:
                self.log.info(_('Skipping installing %s: already installed' % package))
            else:
                pkg.mark_install()
                self.log.info(_('Marking %s for installation' % package))
        except KeyError:
            self.log.info(_("Couldn\'t find a package called %s: skipping" % package))


    def mark_pkg_remove(self, package):
        try:
            pkg = self.cache[package]
            if not pkg.is_installed:
                self.log.info(_('Skipping removing %s: already not-installed' % package))
            else:
                pkg.mark_delete()
                self.log.info(_('Marking %s for removal' % package))
        except KeyError:
            self.log.info(_("Couldn\'t find a package called %s: skipping" % package))


    def install_pkgs(self):
        try:
            self.cache.commit()
        except:
            self.log.exception(_("Package installation failed."))
            self.cache_unlock()

    def get_to_root(self):
        output = subprocess.Popen(["/usr/bin/sudo",
                         "/usr/bin/python3",
                         self.plugin_path + "/packages-data/as_root.py",
                         self.kettle.path], stdout=subprocess.PIPE)
        for line in output.stdout:
            print(line.decode("UTF-8")[:-1])
    def run_install(self):
        #code goes here
        self.get_to_root()
