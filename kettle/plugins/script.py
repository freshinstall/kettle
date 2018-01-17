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
# scriptpy - Kettle plugin for running scripts

import os, subprocess, logging

from . import plugin

import gettext
_ = gettext.gettext

class BadKettle(Exception):
    pass

class Script(plugin.Plugin):

    permissions = {'script': True,
                   'root': False,
                   'remove-pkg': False,
                   'system-config': False
                   }
    root_allowed = permissions['root']
    script_dir = ""
    has_root_script = False

    def __init__(self, kettle):
        # Set up some basic logging
        self.log = logging.getLogger('kettle.Plugin.Script')
        self.log.debug(_("Logging set up!"))

        super().__init__(kettle)

        self.permissions = self.kettle.permissions
        self.root_allowed = self.permissions['root']
        self.extract_scripts()
        self.script_dir = os.path.join(self.kettle.tmppath, "data/scripts")
        self.root_script_path = os.path.join(self.script_dir, "root.sh")
        self.has_root_script = os.path.exists(self.root_script_path)

    def extract_scripts(self):
        self.kettle.extract_kettle(path=self.kettle.tmppath)

    def run_script(self, script_path, root=False):
        if root == False:
            subprocess.call([script_path])
        else:
            subprocess.call(["/usr/bin/sudo",
                            script_path])
    def run_install(self):
        script_path_normal = os.path.join(self.script_dir, "script.sh")
        self.log.info(_('Loading script: %s' % script_path_normal))
        self.run_script(script_path_normal)
        if self.root_allowed == True:
            if self.has_root_script == True:
                self.log.warn(_('Root allowed and root script found.'))
                input(_("\n\nThis Kettle has a root script and the " +
                        "root permission is allowed. \n" +
                        "Policy prevents running a root script without " +
                        "previewing. \nPress [enter] to preview... "))
                print(_("\n** BEGIN SCRIPT: **\n**"))
                with open(self.root_script_path) as f:
                    lines = f.readlines()
                    for line in lines:
                        print("** " +line[:-1])
                print(_('**\n** END SCRIPT **'))
                run_root = input(_("\nWARNING! " +
                                   "Scripts with root can perform any actions " +
                                   "you can perform from a\ncommand " +
                                   "line as ROOT. This means it has FULL " +
                                   "ACCESS to your system!\n\nDO NOT allow " +
                                   "this action if you don't fully trust this " +
                                   "kettle and it's author.\n\nDo you want to " +
                                   "allow this action? (yes/No) "))
                if run_root.lower() in ['y', 'yes', 'allow', 'load']:
                    self.run_script(self.root_script_path, root=True)


