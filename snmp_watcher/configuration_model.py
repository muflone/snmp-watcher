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

from .configuration_abstract import ConfigurationAbstract

SECTION_MODEL = 'Model'

OPTION_NAME = 'name'
OPTION_DESCRIPTION = 'description'
OPTION_GROUPS = 'groups'


class ConfigurationModel(ConfigurationAbstract):
    """ConfigurationModel object to load model configuration from file"""
    def __init__(self, filename, include_groups):
        super(self.__class__, self).__init__(filename)
        # Load generic model data
        self.description = self.config.get(SECTION_MODEL, OPTION_DESCRIPTION)
        self.oids = OrderedDict()
        for group in [str.strip() for str in
                      self.config.get(SECTION_MODEL,
                                      OPTION_GROUPS).split(',')]:
            # Include only the selected groups
            if '*' in include_groups or group in include_groups:
                # Load OIDs
                for option in self.config.options(group):
                    self.oids['%s %s' % (group, option)] = self.config.get(
                        group, option)
