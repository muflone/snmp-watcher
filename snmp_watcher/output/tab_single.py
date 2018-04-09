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

from tabulate import tabulate

from ..common import Common


class OutputTabSingle(object):
    """Print a tab for each host"""

    def __init__(self, style):
        self.format_style = style
        print 'Output format %s' % self.__class__.__name__

    def render(self):
        """Print all the hosts"""
        for host in Common.get_hosts():
            print 'Host %s (%s) (%s)' % (host.name,
                                         host.hostname,
                                         host.description)
            try:
                headers = ['Name', 'Value']
                results = []
                snmp_values = host.get_values()
                for key in snmp_values.keys():
                    value = snmp_values[key]
                    results.append((value.name, value.value))
            except Exception as error:
                print '  Error: %s' % error
            print tabulate(results,
                           headers=headers,
                           tablefmt=self.format_style)
