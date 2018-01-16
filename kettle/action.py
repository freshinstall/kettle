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
# action.py - actions to take

import logging, os
import gettext
_ = gettext.gettext

# generic action class
class Action():

    def __init__(self, kettle):
        # Set up some basic logging
        self.log = logging.getLogger('kettle.Action')
        self.log.debug(_("Logging set up!"))

        self.kettle = kettle

    def create(self, path):
        self.log.debug(_("Starting creation of new kettle:  %s" % path))

        # do some stuff

        self.log.debug(_("%s created!" % path))

    def extract(self, path=None):
        extpath = path
        if path == None:
            extpath = self.kettle.tmppath
        self.log.debug(_("Starting extraction of %s to %s" % (self.kettle.ketid, extpath)))

        # do some stuff
        self.kettle.extract_kettle(path=extpath)

        self.log.debug(_("Extracted %s" % self.kettle.ketid))

    def install(self, kettle, debug=False):
        self.log.debug(_('Starting installation of %s, debug mode is %s' % (self.kettle.ketid, debug)))
        
        # do some stuff
        modules = self.kettle.modules
        from kettle.modules.packages import Packages
        pkgs = Packages(kettle)
        pkgs.get_to_root()
        self.log.debug(_('Installed %s' % self.kettle.ketid))
    
    def create(self, path):
        self.log.debug(_("Starting creation of new kettle:  %s" % self.kettle.ketid))

        # do some stuff
        self.kettle.create()
        self.kettle.close()

        self.log.debug(_("%s created!" % self.kettle.ketid))
