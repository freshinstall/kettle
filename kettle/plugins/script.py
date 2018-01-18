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

import os, stat, subprocess, logging

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
    has_script = False

    def __init__(self, kettle):
        # Set up some basic logging
        self.log = logging.getLogger('kettle.Plugin.Script')
        self.log.debug(_("Logging set up!"))

        super().__init__(kettle)

        self.permissions = self.kettle.permissions
        self.extract_scripts()
        self.script_dir = os.path.join(self.kettle.tmppath, "data/scripts")
        self.script_path = os.path.join(self.script_dir, "script.sh")
        self.has_script = os.path.exists(self.script_path)

    def extract_scripts(self):
        self.kettle.extract_kettle(path=self.kettle.tmppath)

    def set_script_perms(self, script):
        os.chmod(script, stat.S_IXUSR)
        os.chmod(script, stat.S_IXGRP)

    def run_script(self, to_run, root=False):
        self.set_script_perms(to_run)
        if root == False:
            subprocess.call(["/bin/rbash", to_run])
        else:
            subprocess.call(["/usr/bin/sudo",
                             "/bin/rbash",
                             to_run])

    def print_warning_message(self):
        print(_("\n\nThe Script module gives control of your system to the " +
                "scripts provided by this \nkettle. This is potentially " +
                "dangerous, and you should be extremely careful when \ndoing " +
                "this. \nOnly allow running this script if you are sure that " +
                "you trust this kettle and \nits author. For questions, " +
                "contact the author. You can find the contact \ninformation " +
                "by running 'kettle info kettle-name.ket'\n\nFor security, " +
                "the script will be printed to the screen. Please review the " +
                "script\nfor anything potentially dangerous (like 'sudo', " +
                "'su', 'bash', 'rm', etc)."))

    def print_script(self, to_print):
        print(_("\n** BEGIN SCRIPT: **\n**"))
        with open(to_print, "r") as in_file:
            in_lines = in_file.readlines()
        for line in in_lines:
            print("** " + line[:-1])
        print(_("**\n** END SCRIPT **\n\n"))

    def clear_sudo(self):
        subprocess.call(["/usr/bin/sudo", "-k"])

    def run_install(self):
        self.log.info(_("Clearing any existing sudo permissions"))
        self.clear_sudo()
        self.print_warning_message()
        input(_("Press [enter] to review the script... "))
        self.print_script(self.script_path)
        runit = input(_("Do you want to run this script? (yes/No): "))
        if runit.lower() in ['y', 'yes', 'allow', 'run']:
            self.run_script(self.script_path)
