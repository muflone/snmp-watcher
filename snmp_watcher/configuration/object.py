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

import ConfigParser


class ConfigurationObject(object):
    """ConfigurationObject object to load configuration"""
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.optionxform = str

    def read_from_filename(self, filename):
        """Read the configuration data from a file"""
        self.config.read(filename)

    def get(self, section, option):
        """Return a string value from a configuration object"""
        return self.config.get(section, option)

    def set(self, section, option, value):
        """Set a string value for configuration object"""
        return self.config.set(section, option, value)

    def get_int(self, section, option):
        """Return an int value from configuration object"""
        return self.config.getint(section, option)

    def set_int(self, section, option, value):
        """Set an int value for configuration object"""
        return self.config.setint(section, option, value)

    def get_bool(self, section, option):
        """Return a boolean value from configuration object"""
        return self.config.getboolean(section, option)

    def set_bool(self, section, option, value):
        """Set a boolean value for configuration object"""
        return self.config.setboolean(section, option, value)

    def get_float(self, section, option):
        """Return a float value from configuration file"""
        return self.config.getfloat(section, option)

    def set_float(self, section, option, value):
        """Set a float value for configuration file"""
        return self.config.setfloat(section, option, value)
