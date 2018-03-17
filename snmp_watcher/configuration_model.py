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

from collections import OrderedDict

from .configuration_object import ConfigurationObject

SECTION_GENERAL = 'General'

OPTION_NAME = 'name'
OPTION_DESCRIPTION = 'description'
OPTION_AUTODETECT = 'autodetect'


class ConfigurationModel(ConfigurationObject):
    """ConfigurationModel object to load model configuration from file"""
    def __init__(self, name, filename, include_groups):
        super(self.__class__, self).__init__()
        self.read_from_filename(filename)
        # Load generic model data
        self.name = name
        self.filename = filename
        self.description = self.config.get(SECTION_GENERAL, OPTION_DESCRIPTION)
        self.oids = OrderedDict()
        # OID for model Auto detection
        self.autodetect_oid = None
        self.autodetect_value = None
        if self.config.has_option(SECTION_GENERAL, OPTION_AUTODETECT):
            value = self.config.get(SECTION_GENERAL, OPTION_AUTODETECT)
            if '=' in value:
                self.autodetect_oid, self.autodetect_value = [
                    v.strip() for v in value.split('=', 1)]
        # Cycle all the available sections
        for group in [section.strip() for section in self.config.sections()
                      if section not in (SECTION_GENERAL, )]:
            # Include only the selected groups
            if '*' in include_groups or group in include_groups:
                # Load OIDs
                for option in self.config.options(group):
                    self.oids['%s %s' % (group, option)] = self.config.get(
                        group, option)
