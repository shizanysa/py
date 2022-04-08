#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
__author__ = 'shizanysa'
__version__ = '1.0'

import datetime
import os
from zabbix_api import ZabbixAPI
from pprint import pprint

#Define zabbix config file

zbx_conf_file =os.path.dirname(os.path.realpath(__file__)) + '/../conf/zabbix.conf'

# Get zabbix server connect credentials
for tmp_line in open(zbx_conf_file):
    if "server" in tmp_line: zbx_server = str(tmp_line.split("=")[1]).rstrip()
    if "user" in tmp_line: zbx_user = str(tmp_line.split("=")[1]).rstrip()
    if "pass" in tmp_line: zbx_pass = str(tmp_line.split("=")[1]).rstrip()

# Connect to server
zapi = ZabbixAPI(zbx_server)
zapi.login(zbx_user,zbx_pass)

zbx_all_proxy_get = zapi.proxy.get(
        {
            "output": ["host","proxyid"]
            }
        )
for show_proxy in zbx_all_proxy_get:
    print(show_proxy["host"],show_proxy["proxyid"])
