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

from .object import ConfigurationObject
from ..common import Common
from ..snmp.snmp import SNMP


SECTION_HOST = 'Host'

OPTION_NAME = 'name'
OPTION_DESCRIPTION = 'description'
OPTION_HOSTNAME = 'hostname'
OPTION_PORT = 'port'
OPTION_VERSION = 'version'
OPTION_COMMUNITY = 'community'
OPTION_MODEL = 'model'


class ConfigurationHost(ConfigurationObject):
    """ConfigurationHost object to load host from a configuration object"""
    def __init__(self):
        """Initialize object"""
        super(self.__class__, self).__init__()
        self.name = None
        self.description = None
        self.hostname = None
        self.port = None
        self.version = None
        self.community = None
        self.model = None

    def load(self):
        """Load data from configuration"""
        self.name = self.get(SECTION_HOST, OPTION_NAME)
        self.description = self.get(SECTION_HOST, OPTION_DESCRIPTION)
        self.hostname = self.get(SECTION_HOST, OPTION_HOSTNAME)
        self.port = self.get_int(SECTION_HOST, OPTION_PORT)
        self.version = self.get(SECTION_HOST, OPTION_VERSION)
        self.community = self.get(SECTION_HOST, OPTION_COMMUNITY)
        model_name = self.get(SECTION_HOST, OPTION_MODEL)
        self.model = Common.get_model(model_name)

    def set_options(self, destination, description, port, version, community):
        """Set data for host autodetection"""
        self.name = destination
        self.description = description
        self.hostname = destination
        self.port = port
        self.version = version
        self.community = community

    def set_model(self, model_name):
        """Set model"""
        self.model = Common.get_model(model_name)

    def get_values(self):
        """Get the values for the model OIDs via SNMP"""
        return self.get_values_from_oids(self.model.oids)

    def get_values_from_oids(self, oids):
        """Get the requested values from OIDs list"""
        snmp = SNMP(host=self)
        return snmp.get_values(oids)
