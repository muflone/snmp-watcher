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

from pysnmp.hlapi import (
    getCmd,
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectIdentity,
    ObjectType
)

from snmp_value import SNMPValue

class SNMP(object):
    """SNMP object which interacts with PySNMP to get information via SNMP"""
    def __init__(self, hostname, port, version, community):
        self.hostname = hostname
        self.port = port
        self.version = version
        self.community = community
        print self.hostname, self.port, self.version, self.community

    def get_values(self, values):
        """Get SNMP values"""
        results = {}
        oids = []
        for oid in values:
            oids.append(ObjectType(ObjectIdentity('SNMPv2-MIB', oid, 0)))
        # Instance a SNMP GET command
        cmdgen = getCmd(SnmpEngine(),
                        CommunityData(self.community),
                        UdpTransportTarget((self.hostname, self.port)),
                        ContextData(),
                        *oids
                       )
        # Results are in the first iter of the generator
        errorIndication, errorStatus, errorIndex, varBinds = next(cmdgen)
        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
            return None
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                ))
            else:
                # Check if the returned variables and the same number of OIDs
                assert(len(varBinds) == len(oids))
                # Return data from variables
                for index in xrange(len(varBinds)):
                    name = values[index]
                    results[name] = SNMPValue(name, varBinds[index])
            return results
