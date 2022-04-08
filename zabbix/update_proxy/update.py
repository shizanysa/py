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

proxy_old_name = "proxy02"
proxy_new_id = "10335"
proxy_new_ip = "192.168.0.171"

zbx_proxy_get = zapi.proxy.get(
    {
        "output": ["host","proxyids"],
        "search":
        {
            "host": proxy_old_name
        }
    }
)
for proxy_id in zbx_proxy_get:
    print(proxy_id["host"],proxy_id["proxyid"])
    zbx_host_get = zapi.host.get(
            {
                "proxyids": proxy_id["proxyid"]
                }
            )
    for host in zbx_host_get:
        zbx_hostinterface_get = zapi.hostinterface.get(
                {
                    "output": ['interfaceid'],
                    "hostids": host['hostid']
                    }
                )
        for host_ip in zbx_hostinterface_get:
            zbx_hostinterface_update = zapi.hostinterface.update(
                    {
                        "interfaceid": host_ip['interfaceid'],
                        "ip": proxy_new_ip
                        }
                    )
            zbx_host_update = zapi.host.update(
                    {
                        "hostid": host["hostid"],
                        "proxy_hostid": proxy_new_id
                        }
                    )

