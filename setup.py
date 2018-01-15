#!/usr/bin/python3

from distutils.core import setup

setup(
    name = 'kettle',
    version = '0.0.1',
    author = 'kettle',
    description = 'Kettle is a desktop configuration manager',
    url = 'https://github.com/freshinstall/freshinstall',
    license = 'ISC-based',
    scripts = ['kettle/kettle'],
    packages = ['kettle', 'kettle.modules'],
    package_data={'kettle.modules': ["**/*.py"]}
)
