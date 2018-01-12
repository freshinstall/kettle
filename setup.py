#!/usr/bin/python3

from disutils.core import setup

setup(
    name = 'freshinstall',
    version = '0.0.1',
    author = 'freshinstall',
    description = 'Freshinstall is a desktop configuration manager',
    url = 'https://github.com/freshinstall/freshinstall',
    license = 'ISC-based'
    scripts = ['freshinstall/freshinstall'],
    packages = ['freshinstall'],
)
