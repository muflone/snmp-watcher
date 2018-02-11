#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##
#     Project: SNMP Watcher
# Description: Watch devices through SNMP
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

from distutils.core import setup, Command
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data
from distutils.log import info

import os
import os.path
import shutil
import subprocess
from itertools import chain
from glob import glob

from gcentralaccess.constants import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    APP_AUTHOR, APP_AUTHOR_EMAIL, APP_URL)


class Install_Scripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        "Rename main executable python script without .py extension"
        for script in self.get_outputs():
            if script.endswith(".py"):
                info('renaming the python script %s -> %s' % (
                    script, script[:-3]))
                shutil.move(script, script[:-3])


class Install_Data(install_data):
    def run(self):
        install_data.run(self)


setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    maintainer=APP_AUTHOR,
    maintainer_email=APP_AUTHOR_EMAIL,
    url=APP_URL,
    description=APP_DESCRIPTION,
    license='GPL v2',
    scripts=['snmp-watcher.py'],
    packages=['snmp_watcher', ],
    data_files=[],
    cmdclass={
        'install_scripts': Install_Scripts,
    }
)
