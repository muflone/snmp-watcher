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

import snmp_watcher.common
from .configuration_abstract import ConfigurationAbstract
from .snmp import SNMP


SECTION_HOST = 'Host'

OPTION_NAME = 'name'
OPTION_DESCRIPTION = 'description'
OPTION_HOSTNAME = 'hostname'
OPTION_PORT = 'port'
OPTION_VERSION = 'version'
OPTION_COMMUNITY = 'community'
OPTION_MODEL = 'model'


class ConfigurationHost(ConfigurationAbstract):
    """ConfigurationHost object to load host configuration from file"""
    def __init__(self, filename):
        super(self.__class__, self).__init__(filename)
        # Load generic model data
        self.name = self.config.get(SECTION_HOST, OPTION_NAME)
        self.description = self.config.get(SECTION_HOST, OPTION_DESCRIPTION)
        self.hostname = self.config.get(SECTION_HOST, OPTION_HOSTNAME)
        self.port = self.config.getint(SECTION_HOST, OPTION_PORT)
        self.version = self.config.get(SECTION_HOST, OPTION_VERSION)
        self.community = self.config.get(SECTION_HOST, OPTION_COMMUNITY)
        model_name = self.config.get(SECTION_HOST, OPTION_MODEL)
        self.model = snmp_watcher.common.models[model_name]

    def get_values(self):
        """Get the values for the model OIDs via SNMP"""
        snmp = SNMP(host=self)
        return snmp.get_values(self.model.oids)
