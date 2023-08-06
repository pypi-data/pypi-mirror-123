#!/usr/bin/python3
#
# Script to simulate a Zabbix active agent
#

import configparser
import socket
import json
import struct
import logging
import time
import random
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
port = 10051

# Get Python Config parser
config = configparser.RawConfigParser()
config_file = "zabbix-agent-sim.ini"
logging.info('ConfigPath = ' + config_file)
logging.basicConfig(level=logging.INFO)

session_num = random.getrandbits(64)

# Send the message to the Zabbix server
def send_message(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((zabbix_server, port))
    logging.debug("packet %s" % data)
    s.sendall(data)
    data = s.recv(10000)
    s.close()
    # Print the received message
    receive_message = data[13:]
    parsed = json.loads(receive_message)
    logging.debug(parsed["response"])
    return parsed


def active_checks(host_check: str):
    data = dict(request="active checks", host=host_check)
    json_data = json.dumps(data, sort_keys=False)
    logging.debug("data %s" % json_data)
    packet = b'ZBXD\1' + struct.pack('<Q', len(json_data)) + json_data.encode("utf-8")
    logging.debug("packet %s" % packet)
    received_data = send_message(packet)
    
    logging.debug(received_data)
    for x in received_data["data"]:
        logging.debug(str(x["key"]) + " " + str(x["delay"]))
    return received_data["data"]


def agent_data(session_num, config):
    logging.debug("agent_data")
    epoch_time = int(time.time())

    item_id = 1
    # Send data for each host
    data_list = []
    for host in config.sections():
        if host != 'SYSTEM':
            metrics = config.items(host)
            logging.info(metrics)
            # Send metrics to Zabbix
            for key, value in metrics:
                item_data = dict(host=host, key=key, value=value, id=item_id, clock=epoch_time, ns=0)
                data_list.append(item_data)
                item_id += 1
                logging.debug(item_data)

    data = dict(request="agent data", session=session_num, clock=epoch_time, ns=0, data=data_list)
    logging.debug(data)
    json_data = json.dumps(data, sort_keys=False, indent=2)
    logging.debug("data %s" % json_data)
    packet = b'ZBXD\1' + struct.pack('<Q', len(json_data)) + json_data.encode("utf-8")
    received_data = send_message(packet)

    logging.debug(received_data["info"])
    session_num += 1
    return session_num


config.read(config_file)

zabbix_server = config.get('SYSTEM', 'zabbix_server')

checks = active_checks("rpi")

while True:
    # read config file from folder for each loop
    config.read(config_file)
    state = config.get('SYSTEM', 'state')
    # exit if state = stop
    if state == 'stop':
        break

    fetch_keys_val -= 1
    logging.warning('fetch_keys_val = ' + str(fetch_keys_val))
    if fetch_keys_val == 0:
        fetch_keys_val = fetch_keys_time / sleep_value
        logging.warning('fetch_keys_val = ' + str(fetch_keys_val))
        checks = active_checks("rpi")

    session_num = agent_data(session_num, config)

    # sleep
    time.sleep(sleep_value)
