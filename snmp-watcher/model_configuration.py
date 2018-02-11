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

SECTION_MODEL = 'Model'
SECTION_OIDS = 'OIDS'

OPTION_NAME = 'name'
OPTION_DESCRIPTION = 'description'

class ModelConfiguration(object):
    """ModelConfiguration object to load model configuration from file"""
    def __init__(self, filename):
        config = ConfigParser.RawConfigParser()
        # Read data from the configuration file
        config.read(filename)
        # Load generic model data
        self.name = config.get(SECTION_MODEL, OPTION_NAME)
        self.description = config.get(SECTION_MODEL, OPTION_DESCRIPTION)
        # Load OIDs from the OIDS section
        self.oids = {}
        for option in config.options(SECTION_OIDS):
            self.oids[option] = config.get(SECTION_OIDS, option)
