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

from snmp_watcher.common import Common
from snmp_watcher.constants import DIR_MODELS

from snmp_watcher.configuration.object import ConfigurationObject
from snmp_watcher.configuration.model import ConfigurationModel
from snmp_watcher.configuration.host import ConfigurationHost

# Parse command line arguments
parser = argparse.ArgumentParser(description='Read SNMP values')
parser.add_argument('-g', '--group',
                    type=str,
                    dest='groups',
                    action='append',
                    help='values group to monitor')
parser.add_argument('-m', '--models',
                    type=str,
                    dest='models',
                    action='store',
                    help='path where to search for models')
parser.add_argument('-a', '--autodetect',
                    dest='autodetect',
                    action='store_true',
                    help='autodetection mode')
parser.add_argument('destinations',
                    type=str,
                    action='store',
                    nargs='+',
                    help='destination host or configuration file')
# Add arguments for autodetection mode
parser_group = parser.add_argument_group('Autodetection options')
parser_group.add_argument('-v', '--version',
                          type=str,
                          action='store',
                          choices=('1', '2c'),
                          default='1',
                          help='SNMP version to use')
parser_group.add_argument('-c', '--community',
                          type=str,
                          action='store',
                          default='public',
                          help='community string to use')
parser_group.add_argument('-p', '--port',
                          type=int,
                          action='store',
                          default='161',
                          help='UDP port number for SNMP request')
parser_group.add_argument('-n', '--no-scan',
                          dest='no_scan',
                          action='store_true',
                          help='find model only, don\'t read values')
parser_group.add_argument('-M', '--model',
                          type=str,
                          dest='model',
                          action='store',
                          help='use the specified model')
# Add arguments for autodetection mode
parser_group = parser.add_argument_group('Output options')
parser_group.add_argument('-o', '--output',
                          type=str,
                          action='store',
                          choices=('sequence', 'tab_single', 'tab_multiple'),
                          default='sequence',
                          help='output format to use')
arguments = parser.parse_args()
# If no groups were specified list all services groups
if not arguments.groups:
    arguments.groups = ['*']

# Load models
autodetections = {}
for filename in os.listdir(arguments.models or DIR_MODELS):
    model_name = filename.split('.conf')[0]
    model = ConfigurationModel(name=model_name,
                               filename=os.path.join(DIR_MODELS, filename),
                               include_groups=arguments.groups)
    if model.autodetect_oid:
        autodetections[model.name] = {'oid': model.autodetect_oid,
                                      'value': model.autodetect_value
                                      }
    Common.set_model(model_name, model)

for item in arguments.destinations:
    if arguments.model:
        # Use specific model mode
        host = ConfigurationHost()
        host.set_options(destination=item,
                         description='manual model selection for %s' % item,
                         port=arguments.port,
                         version=arguments.version,
                         community=arguments.community)
        host.set_model(arguments.model)
        # Add host to the list of hosts to check
        Common.add_host(host)
    elif arguments.autodetect:
        # Autodetection mode
        host = ConfigurationHost()
        host.set_options(destination=item,
                         description='autodetection for %s' % item,
                         port=arguments.port,
                         version=arguments.version,
                         community=arguments.community)
        try:
            values = host.get_values_from_oids(
                dict((key, autodetections[key]['oid'])
                     for key in autodetections.keys()))
            # Search for a reply with the same OID and value
            model_found = None
            for key in values:
                # Skip "No Such Object currently exists at this OID" replies
                if key != 'NOT FOUND' and values[key].is_valid():
                    requested_oid = autodetections[key]['oid']
                    requested_value = autodetections[key]['value']
                    # Check for the same (meta) OID and values
                    if (requested_oid == values[key].meta_oid and
                            requested_value == values[key].value):
                        # Model was found
                        model_found = key
                        break
                # No further searches are needed
                if model_found:
                    break
            assert model_found, 'model not found'
            if model_found:
                host.set_model(model_found)
                if arguments.no_scan:
                    # Show only the detected model
                    print 'Host %s, model detected: %s' % (host.name,
                                                           model_found)
                else:
                    # Add host to the list of hosts to check
                    Common.add_host(host)
        except Exception as error:
            print 'Host %s' % (host.name, )
            print '  Error: %s' % error
    else:
        # Usage with configuration files
        assert os.path.exists(item)
        if os.path.isfile(item):
            # Load a single configuration file
            host = ConfigurationHost()
            host.read_from_filename(item)
            host.load()
            Common.add_host(host)
        else:
            print '%s is not a file, it will be skipped' % item


# Print results
for host in Common.get_hosts():
    print 'Host %s (%s) (%s)' % (host.name, host.hostname, host.description)
    try:
        values = host.get_values()
        for key in values.keys():
            value = values[key]
            print '  %s = %s' % (value.name, value.value)
    except Exception as error:
        print '  Error: %s' % error
