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
# config.py - Kettle configuration files manager

import shutil, os, subprocess, tarfile
import logging
from pathlib import Path

from . import plugin

import gettext
_ = gettext.gettext

class Config(plugin.Plugin):

    def __init__(self, kettle):
        super().__init__(kettle)
        self.log = logging.getLogger("kettle.Plugin.Config")
        self.log.debug(_("Logging set up!"))
        self.permissions = self.kettle.permissions
        self.sys_config_path = os.path.join(self.kettle.tmppath, "/data/config/system.tar")
        self.usr_config_path = self.kettle.tmppath + "/data/config/home.tar"
        self.has_sys_config = os.path.isdir(self.sys_config_path)

        self.user_home = str(Path.home()) + "/"

    def restore_home_configuration(self):
        self.log.info(_("Restoring user configuration"))
        self.kettle.extract_kettle(path=self.kettle.tmppath)
        usr_config_ark = tarfile.open(self.user_config_path, mode="r")
        usr_config_ark.extractall(path=self.user_home)
        self.log.info(_("User config restoration complete!"))

    def restore_sys_configuration(self):
        self.kettle.extract_kettle()
        shutil.copytree(self.sys_config_path,
                        "/", symlinks=True)

    def get_to_root(self):
        self.log.info(_("Restoring system configuration"))
        subprocess.call(["/usr/bin/sudo",
                         "/usr/bin/python3",
                         self.plugin_path + "/config-data/as_root.py",
                         self.kettle.path])
        self.log.info(_("System config restoration complete!"))

    def run_install(self):
        self.restore_home_configuration()
        if self.has_sys_config == True:
            if self.permissions['system-config'] == True:
                self.get_to_root()
