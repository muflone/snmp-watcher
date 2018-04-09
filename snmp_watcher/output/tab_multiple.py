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

from tabulate import tabulate

from ..common import Common


class OutputTabMultiple(object):
    """Print a tab for all the host"""

    def __init__(self, style):
        self.format_style = style
        print 'Output format %s' % self.__class__.__name__

    def render(self):
        """Print all the hosts"""
        hosts_values = OrderedDict()
        headers = ['Host']
        for host in Common.get_hosts():
            values = OrderedDict()
            try:
                snmp_values = host.get_values()
                for key in snmp_values.keys():
                    value = snmp_values[key]
                    if value.name not in headers:
                        headers.append(value.name)
                    values[value.name] = value.value
            except Exception as error:
                print '  Error: %s' % error
            hosts_values[host.name] = values
        # Prepare results
        results = []
        for host in hosts_values.keys():
            host_values = [host]
            for field in headers[1:]:
                host_values.append(hosts_values[host].get(field, ''))
            results.append(host_values)
        print tabulate(results,
                       headers=headers,
                       tablefmt=self.format_style)
