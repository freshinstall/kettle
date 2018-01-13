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

    def extract(self, path):
        self.log.debug(_("Starting installation of %s to %s" % (self.kettle.ketid, self.kettle.tmppath)))

        # do some stuff
        self.kettle.extract_kettle(path=path)

        self.log.debug(_("Installed %s" % self.kettle.ketid))

class Create(Action):

    def __init__(self):
        # Set up some basic logging
        self.log = logging.getLogger('kettle.Action')
        self.log.debug(_("Logging set up!"))

    def create(self, path):
        self.log.debug(_("Starting creation of new kettle:  %s" % path))

        # do some stuff

        self.log.debug(_("%s created!" % path))
