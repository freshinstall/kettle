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

# Here we import some helpful modules to do more stuff with python
import tarfile
import yaml
import glob, os
import logging

# And we set up the translations again.
import gettext
_ = gettext.gettext

# This is for some advanced Error handling.
class BadKettle(Exception):
    pass

# This class is the python representation of a kettle itself.
class Kettle():

    # First we have the attributes. These describe the kettle.
    # All of these are set using the code below this block
    name = ""                 # The name of the kettle, from the yaml file
    ketid = ""                # The id field of the kettle's yaml
    modules = []              # What plugins the kettle will load.
    permissions = {}          # What permissions the kettle requests.
    standard = 0              # The standards version of the kettle
    tmppath = "/tmp/kettle/"  # This is the path in /tmp we'll use if we need to
    kettle_yaml = []          # This is a representation of every field in the
                              # kettle YAML.

    # Next we set up the class's methods. Methods are actions that classes can
    # perform. They work exactly like functions.
    def __init__(self, path):
        # __init__ is the method that is called when we create an object. Any
        # arguments we give to the object will be passed to this method.
        # Additionally, it will set up all of the attributes and get a lot of
        # information. Here we pass the path to the kettle file as the path
        # argument.

        self.path = path # This creates a new attribute of our kettle called "path"
                         # It stores the path of the kettle file. We set it to
                         # The value of the "path" variable we got as
                         # an argument.

        # This is where we open up the Kettle file for reading. Since Kettles are
        # tar archives, we use the tarfile module. Again, we wrap this in a
        # try/except block because we don't yet know if the user gave us a path
        # to a kettle that exists, and need to present an error if it doesn't.
        try:
            # "kettle_ark" is the representation of the kettle archive
            self.kettle_ark = tarfile.open(name=self.path, mode='r')
        except FileNotFoundError:
            # Here we're looking if the above block failed with a
            # "FileNotFoundError" exception, and we're sending out a
            # "BadKettle" exception instead.
            raise BadKettle(_('The kettle doesn\'t exist'))

        # These methods all populate the class attributes with actual information
        self.get_yaml()         # This gets the yaml
        self.get_name()         # This gets the name
        self.get_id()           # This gets the id
        self.get_modules()      # This gets a list of modules the kettle needs
        self.get_permissions()  # This gets the list of permissions the kettle requests.

        # Here we set the tmppath attribute to /tmp/kettle/the_id_of_the_kettle
        self.tmppath = "/tmp/kettle/%s" % self.ketid

    def get_yaml(self):
        try:
            kettle_yaml_info = self.kettle_ark.getmember('metainfo/meta.yaml')
        except KeyError:
            raise BadKettle(_("The kettle is missing meta.yaml"))

        kettle_yaml_b = self.kettle_ark.extractfile(kettle_yaml_info)
        self.kettle_yaml = yaml.safe_load(kettle_yaml_b)

        return self.kettle_yaml

    def get_name(self):
        self.name = self.kettle_yaml['name']
        return self.name

    def get_id(self):
        self.ketid = self.kettle_yaml['id']
        return self.ketid

    def get_modules(self):
        self.modules = self.kettle_yaml['modules']
        return self.modules

    def get_permissions(self):
        self.permissions = self.kettle_yaml['permissions']
        return self.permissions

    def extract_kettle(self, path=tmppath):
        self.kettle_ark.extractall(path=path)

class NewKettle(Kettle):

    name = ""
    ketid = ""
    modules = []
    permissions = {}
    standard = 0
    tmppath = "/tmp/kettle/"
    kettle_yaml = []

    def __init__(self, path):
        self.log = logging.getLogger('kettle.NewKettle')
        self.log.debug(_("Logging set up!"))
        self.path = path
        with open(os.path.join(self.path, "metainfo/meta.yaml")) as f:
            self.kettle_yaml = yaml.safe_load(f)

        self.ketid = self.kettle_yaml['id']
        kettle_filename = ("%s.ket" % self.ketid)

        try:
            self.kettle_ark = tarfile.open(name=kettle_filename, mode='x')
        except FileExistsError:
            raise BadKettle(_('That kettle already exists!'))

    def create(self):
        self.log.info(_("Adding %s to kettle" % self.path))
        os.chdir(self.path)
        self.kettle_ark.add("data")
        self.kettle_ark.add("metainfo")

    def close(self):
        self.kettle_ark.close()
