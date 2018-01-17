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
# action.py - actions to take

import logging, os, importlib
import gettext
_ = gettext.gettext

# generic action class
class Action():

    trusted_plugins = ['packages']
    untrusted_response = {"Y" : True,
                          "y" : True,
                          "yes" : True,
                          "Yes" : True,
                          "true" : True,
                          "True" : True,
                          }


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
        
        modules = self.kettle.modules
        # Module introspection
        for i in modules:
            if not i in self.trusted_plugins:
                allow_response = input(_(
                                        "\n\nThe kettle uses the %s plugin which is not a trusted plugin. \n" % i +
                                        "Do you want to allow loading this module, or skip it? (yes/Skip): "))
                if not allow_response.lower() in ('y', 'yes', 'allow', 'load'):
                    continue
            try:
                current_module = importlib.import_module('kettle.modules.' + i)
                current_class = getattr(current_module, i.capitalize())
                current_object = current_class(kettle)
                self.log.info(_("Loaded module: %s" % i))
                current_object.run_install()
                self.log.info(_("Module %s complete!" % i))
            except ModuleNotFoundError:
                self.log.error(_("Couldn't find module: %s" % i))
                pass
        self.log.debug(_('Installed %s' % self.kettle.ketid))
    
    def create(self, path):
        self.log.debug(_("Starting creation of new kettle:  %s" % self.kettle.ketid))

        # do some stuff
        self.kettle.create()
        self.kettle.close()

        self.log.debug(_("%s created!" % self.kettle.ketid))
