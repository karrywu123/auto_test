#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib
import  urllib.request
import urllib.parse
import itertools
import time
import hashlib
import requests
import sys
import json
'''
客户编号

用户名

'''

head = {'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': ''} #Production

class Godaddy_API(object):
    def __init__(self):
        self.head = head
    #列出账号下所有的域名
    def list_all_domains(self):
        url = 'https://api.godaddy.com/v1/domains'
        req = requests.get(url, headers=self.head)
        return req.json()
    #列出域名的详细记录
    def list_domains_detail(self,domain):
        url = 'https://api.godaddy.com/v1/domains/' + domain
        req = requests.get(url, headers=self.head)
        return req.json()
    #更新域名的NS记录
    def update_domains_ns(self,domain,nameServer):
        url = 'https://api.godaddy.com/v1/domains/' + domain
        nsdata = nameServer.split(',')
        data = {"locked": True, "nameServers": nsdata, "renewAuto": True, "subaccountId": ''}
        data = json.dumps(data)
        data01 = str(data)
        req=requests.patch(url, data=data01, headers=self.head)

        return req.json()

if __name__ == '__main__':
    g = Godaddy_API()
    for i in g.list_all_domains():
        print(i)
        print(i['domainId'], i['domain'], i['status'], i['expires'])
    #print(g.list_domains_detail(''))



