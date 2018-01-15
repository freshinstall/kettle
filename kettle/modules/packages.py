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
# packages.py - Kettle apt packages module

import apt
import sys

from .modules import Module

class Packages(Module):

    cache = apt.cache.Cache()

    def cache_lock(self):
        self.cache.update()
        self.cache.open()

    def cache_unlock(self):
        self.cache.close()

    def mark_pkg_install(self, package):
        pkg = cache[package]
        if pkg.is_installed:
            self.log.info(_('Skipping installing %s: already installed' % package))
        else:
            pkg.mark_install()
            self.log.info(_('Marking %s for installation' % package))

    def mark_pkg_remove(self, package):
        pkg = cache[package]
        if not pkg.is_installed:
            self.log.info(_('Skipping removing %s: already not-installed' % package))
        else:
            pkg.mark_delete()
            self.log.info(_('Marking %s for removal' % package))

    def install_pkgs(self):
        try:
            self.cache.commit()
        except Exception, arg:
            self.log.exception(_("Package installation failed.")
            self.cache_unlock()
