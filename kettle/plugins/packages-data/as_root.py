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
# as_root.py - Things to do as root for a module

import sys

from kettle.ket import Kettle
from kettle.plugins.packages import Packages

kettle = Kettle(sys.argv[1])
pkgs = Packages(kettle)
pkgs.get_pkgs()
pkgs.cache_lock()
for i in pkgs.package_install:
    pkgs.mark_pkg_install(i)
for i in pkgs.package_remove:
    pkgs.mark_pkg_remove(i)
pkgs.install_pkgs()
pkgs.cache_unlock()
