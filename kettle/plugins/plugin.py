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
# plugin.py - A base class for kettle plugins

import os
import gettext
_ = gettext.gettext

class Plugin():

    plugin_path = os.path.dirname(os.path.realpath(__file__))
    permissions = {'script': True,
                   'root': True,
                   'remove-pkg': True,
                   'system-config': True
                   }

    def __init__(self, kettle):

        self.kettle = kettle
        self.kettle_ark = self.kettle.kettle_ark

    def list_permissions(self):
        return self.permissions

    def run_install(self):
        raise NotImplementedError

    def run_remove(self):
        raise NotImplementedError
