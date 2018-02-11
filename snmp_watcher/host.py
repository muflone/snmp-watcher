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

from .snmp import SNMP


class Host(object):
    """
    Host object which contains host address, SNMP port, SNMP version and
    SNMP community string.
    """
    def __init__(self, hostname, port, version='v2c', community='public'):
        self.hostname = hostname
        self.port = port
        self.version = version
        self.community = community

    @property
    def version(self):
        """Get SNMP version protocol"""
        return self._version

    @version.setter
    def version(self, value):
        """Set SNMP version protocol"""
        if value not in ('v1', 'v2c'):
            raise ValueError("Versions allowed are 'v1' and 'v2c'")
        self._version = value

    @property
    def port(self):
        """Get SNMP port number"""
        return self._port

    @port.setter
    def port(self, value):
        """Set SNMP port number"""
        if value not in range(1, 65536):
            raise ValueError("Port number not allowed")
        self._port = value

    def get_values(self, oids):
        """Get SNMP values from the host"""
        snmp = SNMP(hostname=self.hostname,
                    port=self.port,
                    version=self.version,
                    community=self.community)
        return snmp.get_values(oids)
