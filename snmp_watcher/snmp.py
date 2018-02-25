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

from pysnmp.hlapi import (
    getCmd,
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectIdentity,
    ObjectType
)

from .snmp_value import SNMPValue


class SNMP(object):
    """SNMP object which interacts with PySNMP to get information via SNMP"""
    def __init__(self, host):
        self.host = host

    def get_values(self, values):
        """Get SNMP values"""
        results = OrderedDict()
        oids = []
        for key in values.keys():
            oid = values[key]
            # Apply common replacements
            oid = oid.replace('SNMPv2-SMI::enterprises.', '.1.3.6.1.4.1.', 1)
            oid = oid.replace('IP-MIB::ip.', '.1.3.6.1.2.1.4.', 1)
            if oid.startswith('mib-2.'):
                oid = oid.replace('mib-2.', '.1.3.6.1.2.1.', 1)
            if '::' in oid:
                mib, oid = oid.split('::', 1)
                if ':' in oid:
                    # Use MIB, OID and subtype
                    oid, subtype = oid.split(':', 1)
                    oids.append(ObjectType(ObjectIdentity(mib, oid, subtype)))
                else:
                    # Use MIB and OID
                    oids.append(ObjectType(ObjectIdentity(mib, oid)))
            else:
                # Just use plain OID
                oids.append(ObjectType(ObjectIdentity(oid)))
        # Instance a SNMP GET command
        cmdgen = getCmd(SnmpEngine(),
                        CommunityData(self.host.community),
                        UdpTransportTarget((self.host.hostname,
                                            self.host.port)),
                        ContextData(),
                        *oids
                        )
        # Results are in the first iter of the generator
        errorIndication, errorStatus, errorIndex, varBinds = next(cmdgen)
        # Check for errors and print out results
        if errorIndication:
            raise Exception(errorIndication)
        else:
            if errorStatus:
                raise Exception('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                ))
            else:
                # Check if the returned variables and the same number of OIDs
                assert(len(varBinds) == len(oids))
                # Return data from variables
                keys = values.keys()
                for index in xrange(len(varBinds)):
                    name = keys[index]
                    results[name] = SNMPValue(name, varBinds[index])
            return results
