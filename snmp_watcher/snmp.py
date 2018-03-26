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
from socket import gethostbyname
from datetime import datetime

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
        # Extract special values
        values = OrderedDict(values)
        special_values = {
            '{name}': self.host.name,
            '{description}': self.host.description,
            '{model}': self.host.model.name if self.host.model else 'None',
            '{hostname}': self.host.hostname,
            '{address}': gethostbyname(self.host.hostname),
            '{port}': self.host.port,
            '{version}': self.host.version,
            '{community}': self.host.community,
            '{date}': datetime.now().strftime('%Y/%m/%d'),
            '{time}': datetime.now().strftime('%H:%M:%S'),
            '{now}': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        }
        for key in values.keys():
            value = values[key]
            if value in special_values.keys():
                # Add special value to the results
                results[key] = SNMPValue(meta_oid=key,
                                         name=key,
                                         value=special_values[value])
                # Removes special values from OIDs list
                values.pop(key)
        # Scan SNMP value
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
                        CommunityData(self.host.community,
                                      mpModel={'1': 0,
                                               '2c': 1
                                              }[self.host.version]),
                        UdpTransportTarget((self.host.hostname,
                                            self.host.port)),
                        ContextData()
                        )
        next(cmdgen)
        # Get each value
        keys = values.keys()
        for index in xrange(len(keys)):
            name = keys[index]
            # Request a single value from the cmdgen object
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.send(
                (oids[index],))
            # Check for errors
            if errorIndication:
                raise Exception(errorIndication)
            # If v1 version was requested we can safely ignore errorStatus = 2
            # for "No Such Object currently exists at this OID" errors
            if errorStatus and (self.host.version == '1' and errorStatus != 2):
                raise Exception('%d at %s' % (
                    errorStatus,
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                ))
            else:
                # Get data from variable
                keys = values.keys()
                name = keys[index]
                results[name] = SNMPValue(meta_oid=values[name],
                                          name=name,
                                          value=varBinds[0])
        # Return the gathered results
        return results
