#!/usr/bin/env python3

import configparser
import yaml
import zabbix_api

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    if s.isnumeric():
        return int(s)
    else:
        return int(s[:-1]) * seconds_per_unit[s[-1]]

config_parser = configparser.RawConfigParser()

# Read the config
config_parser.read("zabbix-agent-rec.ini")
ZABBIX_SERVER = config_parser.get('SYSTEM', 'zabbix_server')
ZABBIX_USERNAME = config_parser.get('SYSTEM', 'zabbix_username')
ZABBIX_PASSWORD = config_parser.get('SYSTEM', 'zabbix_password')
HOSTNAME = config_parser.get('SYSTEM', 'hostname')

zapi = zabbix_api.ZabbixAPI(server="http://" + ZABBIX_SERVER + "/zabbix")
zapi.login(ZABBIX_USERNAME, ZABBIX_PASSWORD)

# Get the host
host = zapi.host.get({ "filter": { "host": [ HOSTNAME ] } })

if host[0]:
    hostid = host[0]['hostid']

    # Get the host items
    items = zapi.item.get({
        "output": "extend",
        "hostids": hostid,
        "sortfield": "name",
        "output": [ "key_", "name", "type", "value_type", "lastvalue", "delay" ]
    })

    passive_items = 0
    active_items = 0
    for item in items:
        # 0 - Zabbix agent;
        # 7 - Zabbix agent (active);
        if item['type'] == '0':
            passive_items += 1
        if item['type'] == '7':
            active_items += 1
        item['delay'] = convert_to_seconds(item['delay'])

    # Filter the active and passive zabbix items
    items[:] = [item for item in items if item['type'] == '0' or item['type'] == '7']

    # Add the hostname to the front
    host_items = dict()
    host_items[HOSTNAME] = items

    # Dump the recorded items as yaml
    output = yaml.dump(host_items, Dumper=yaml.Dumper)
    with open(HOSTNAME + '.za', 'w') as writer:
        writer.write(output)

zapi.logout()
