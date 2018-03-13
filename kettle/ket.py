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
# ket.py - Kettle object class

import tarfile
import yaml
import glob, os
import logging

class BadKettle(Exception):
    pass

class Kettle():
    kettle_yaml = {}
    path = '/tmp/kettle'
    data_path = '/tmp/kettle/data'
    meta_path = '/tmp/kettle/metainfo'
    kettle_ark = ""

    def __init__(self, path):

        self.path = path
        self.kettle_ark = self.ark_open()
        self.kettle_yaml = self.get_yaml()


    def ark_open(self):
        try:
            archive = tarfile.open(name=self.path, mode='r')
        except FileNotFoundError as e:
            raise BadKettle('The file doesn\'t exist')

        return archive

    def ark_close(self):
        self.kettle_ark.close()

    def get_yaml(self):
        try:
            kettle_yaml_info = self.kettle_ark.getmember('metainfo/meta.yaml')
        except KeyError as e:
            raise BadKettle('The kettle is missing meta.yaml')

        kettle_yaml_bytes = self.kettle_ark.extractfile(kettle_yaml_info)
        kettle_yaml = yaml.safe_load(kettle_yaml_bytes)

        return kettle_yaml

    def set_paths(self):
        self.data_path = os.path.join(self.path, 'data')
        self.meta_path = os.path.join(self.path, 'metainfo')

    def info(self):
        kettle_info = []
        kettle_info.append(_('Kettle Information:'))
        kettle_info.append(_('  ID: %s' % self.kettle.ketid))
        kettle_info.append(_('  Name: %s' % self.kettle.name))
        kettle_info.append(_('  Author: %s <%s>' % (self.kettle.get_info('author'),
                                                 self.kettle.get_info('email'))))
        kettle_info.append(_('  URL: %s' % self.kettle.get_info('URL')))
        kettle_info.append(_('  Version: %s' % self.kettle.get_info('version')))
        kettle_info.append(_('Plugins:'))
        for plugin in self.kettle.plugins:
            plugin_trusted = _("Untrusted")
            if plugin in self.trusted_plugins:
                plugin_trusted = _("Trusted")
            plugin_info = '        %s, %s' % (plugin, plugin_trusted)
            kettle_info.append(plugin_info)
        kettle_info.append(_('Permissions Requested:'))
        for i in self.kettle.permissions:
            if self.kettle.permissions[i] == True:
                permission = '        %s' % i
                kettle_info.append(permission)
        return kettle_info


class KettleTemplate(Kettle):
    kettle_yaml = {
        'name': 'New Kettle',
        'id': 'new-kettle',
        'description': 'A Kettle to test things out.\n',
        'author': 'kettle',
        'URL': 'https://github.com/freshinstall/kettle',
        'email': 'email@domain',
        'version': '1.0',
        'standard': 0,
        'plugins': ['repos', 'packages', 'config', 'dconf'],
        'permissions': {
            'script': False,
            'root': False,
            'remove-pkg': False,
            'system-config': False}}

    def __init__(self, path='/tmp/kettle', name='New Kettle',
                 ketid='new-kettle', description="New Kettle", author='Kettle',
                 email='kettle@example.com',
                 url='https://github.com/freshinstall/kettle', version='1.0'):

        self.log = logging.getLogger('kettle.NewKettle')

        self.kettle_yaml['name'] = name
        self.kettle_yaml['id'] = ketid
        self.kettle_yaml['author'] = author
        self.kettle_yaml['email'] = email
        self.kettle_yaml['version'] = version
        self.kettle_yaml['URL'] = url

        self.path = path
        self.set_paths()

    def make_paths(self):
        os.makedirs(self.path)
        os.makedirs(self.data_path)
        os.makedirs(self.meta_path)
