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


class Common(object):
    __models = {}
    __hosts = []

    @classmethod
    def get_model(cls, name):
        """Get a model by its name"""
        return cls.__models[name]

    @classmethod
    def set_model(cls, name, model):
        """Set a model"""
        cls.__models[name] = model

    @classmethod
    def add_host(cls, host):
        """Add a new host to the list"""
        cls.__hosts.append(host)

    @classmethod
    def get_hosts(cls):
        """Get the hosts list"""
        return cls.__hosts
