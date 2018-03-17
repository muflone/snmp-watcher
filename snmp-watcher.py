#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

import os
import os.path
import argparse

import snmp_watcher.common
from snmp_watcher.constants import DIR_MODELS
from snmp_watcher.configuration_object import ConfigurationObject
from snmp_watcher.configuration_model import ConfigurationModel
from snmp_watcher.configuration_host import ConfigurationHost

# Parse command line arguments
parser = argparse.ArgumentParser(description='Read SNMP values')
parser.add_argument('-g', '--group', dest='groups', type=str, action='append',
                    help='values group to monitor')
parser.add_argument('-m', '--models', dest='models', type=str, action='store',
                    help='path where to search for models')
parser.add_argument('configuration', type=str, action='store', nargs='+',
                    help='configuration file')
parser.add_argument('-a', '--autodetect', action='store_true',
                    help='autodetection mode')
arguments = parser.parse_args()
# If no groups were specified list all services groups
if not arguments.groups:
    arguments.groups = ['*']

# Load models
autodetections = {'NOT FOUND': {'oid': 'SNMPv2-MIB::sysDescr:0',
                                'value': 'NOT FOUND'}
                 }
for filename in os.listdir(arguments.models or DIR_MODELS):
    model_name = filename.split('.conf')[0]
    model = ConfigurationModel(name=model_name,
                               filename=os.path.join(DIR_MODELS, filename),
                               include_groups=arguments.groups)
    if model.autodetect_oid:
        autodetections[model.name] = { 'oid': model.autodetect_oid,
                                       'value': model.autodetect_value
                                     }
    snmp_watcher.common.models[model_name] = model

for key in snmp_watcher.common.models:
    model = snmp_watcher.common.models[key]

for filename in arguments.configuration:
    if not arguments.autodetect:
        # Usage with configuration files
        assert os.path.exists(filename)
        if os.path.isfile(filename):
            # Load a single configuration file
            host = ConfigurationHost()
            host.read_from_filename(filename)
            host.load()
            snmp_watcher.common.hosts.append(host)
        else:
            print '%s is not a file, it will be skipped' % filename
    else:
        # Autodetection mode
        host = ConfigurationHost()
        host.set_for_autodetection(filename, 161, 'v1', 'public')
        values = host.get_values_from_oids(
            dict((key, autodetections[key]['oid'])
            for key in autodetections.keys()))
        # Search for a reply with the same OID and value
        model_found = None
        # print values
        for key in values:
            # Skip "No Such Object currently exists at this OID" replies
            if key != 'NOT FOUND' and values[key].is_valid():
                requested_oid = autodetections[key]['oid']
                requested_value = autodetections[key]['value']
                # Check for the same (meta) OID and values
                if (requested_oid == values[key].meta_oid and
                        requested_value == values[key].value):
                    model_found = key
                    break
            # No further searches are needed
            if model_found:
                break
        assert model_found, 'model not found'
        if model_found:
            print 'model found:', model_found
            host.set_model(model_found)
            snmp_watcher.common.hosts.append(host)


# Print results
for host in snmp_watcher.common.hosts:
    print 'Host %s (%s) (%s)' % (host.name, host.hostname, host.description)
    try:
        values = host.get_values()
        for key in values.keys():
            value = values[key]
            print '  %s = %s' % (value.name, value.value)
    except Exception as error:
        print '  Error: %s' % error
