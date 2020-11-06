#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib
import urllib.request
import urllib.parse
import itertools
import time
import hashlib
import requests
import sys
import json
values = {'X-Auth-Email': '', 'X-Auth-Key': '', 'Content-Type': 'application/json', 'X-Auth-User-Service-Key': ''}
class cloudflare(object):
    def __init__(self):
        self.public_values = values
        self.Email = self.public_values['X-Auth-Email']
        self.auth_api_key = self.public_values['X-Auth-Key']
        self.user_service_api_key = self.public_values['X-Auth-User-Service-Key']
        self.content_type = self.public_values['Content-Type']
    #获取全部域名的zone_id
    def get_zone_id(self):
        url = "https://api.cloudflare.com/client/v4/zones?page=1&per_page=1000"
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.get(url, headers=val)
        return req.json()
    #选择获取域名的id
    def chice_zone_id(self,domain):
        dict01 = {}
        zone_id=[]
        for i in self.get_zone_id()['result']:
            #print(i)
            key = i['name']
            value = i['id']
            dict01.setdefault(key, value)
        if domain in dict01.keys():
             zone_id.append(dict01[domain])
        else:
            exit("不存在这个域名")
        return zone_id[0]
    #清理域名的缓存
    def Purge_Cache(self,domain):
        id = self.chice_zone_id(domain)
        url = "https://api.cloudflare.com/client/v4/zones/" + id +"/purge_cache"
        data = {"purge_everything": True}
        data = json.dumps(data)
        data1 = str(data)
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type, 'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.post(url, data=data1, headers=val)
        return req.json()
    #域名加记录的
    def add_domain_record(self,type,name,content,domain):
        id = self.chice_zone_id(domain)
        url= 'https://api.cloudflare.com/client/v4/zones/' + id + '/dns_records'
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        data ={"type": type, "name": name, "content": content, "ttl":1, "priority": 10, "proxied": False}
        data = json.dumps(data)
        data1 = str(data)
        req = requests.post(url, data=data1, headers=val)
        return req.json()
    #列出域名所有的记录的ID
    def list_all_domain_record(self,domain):
        id = self.chice_zone_id(domain)
        url01 = "https://api.cloudflare.com/client/v4/zones/" + id + "/dns_records?page=1&per_page=1000"
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type, 'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.get(url01, headers=val)
        return req.json()['result']
    #获取指定域名下面指定的记录ID
    def chioce_domain_record_id(self,domain,record):
        dict01 = {}
        record_id = []
        for i in self.list_all_domain_record(domain):
            key = i['name']
            value = i['id']
            dict01.setdefault(key, value)
        if record in dict01.keys():
            record_id.append(dict01[record])
        else:
            exit("不存在这个记录")
        return record_id[0]
    #删除某个域名的记录
    def del_domain_record(self,domain,record):
        id = self.chice_zone_id(domain)
        record_id = self.chioce_domain_record_id(domain, record)
        url = "https://api.cloudflare.com/client/v4/zones/" + id + "/dns_records/" + record_id
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.delete(url, headers=val)
        return req.json()

    # 列出账号信息
    def list_accounts(self):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        url = "https://api.cloudflare.com/client/v4/accounts?page=1&per_page=20"
        req = requests.get(url, headers=val)
        return req.json()['result'][0]

    #给账号删除域名
    def del_domain_zone(self,domain):
        id = self.chice_zone_id(domain)
        url = "https://api.cloudflare.com/client/v4/zones/" + id
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.delete(url, headers=val)
        return req.json()
    #给账号添加域名
    def create_domain_zone(self,domain):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        account_id = self.list_accounts()['id']
        account_name = self.list_accounts()['name']
        data={"name":domain,"account":{"id":account_id,"name":account_name},"jump_start":True}
        data = json.dumps(data)
        data1 = str(data)
        url = "https://api.cloudflare.com/client/v4/zones"
        req = requests.post(url,data=data1, headers=val)
        return req.json()

    #列出账户下面的所有防火墙规则
    def list_account_Rules(self):
        account_id = self.list_accounts()['id']
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        url = "https://api.cloudflare.com/client/v4/accounts/" + account_id + "/firewall/access_rules/rules?page=1&per_page=1000"
        req = requests.get(url, headers=val)
        return req.json()['result']

    #列出域名下面的所有防火墙规则
    def List_domain_Access_Rules(self,domain):
        id = self.chice_zone_id(domain)
        url = "https://api.cloudflare.com/client/v4/zones/" +id + "/firewall/access_rules/rules?page=1&per_page=1000"
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        req = requests.get(url, headers=val)
        return req.json()['result']

    #给域名下添加防火墙规则
    def add_domain_Rules(self,domain,ip,mode,notes):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type, 'X-Auth-User-Service-Key': self.user_service_api_key}
        id = self.chice_zone_id(domain)
        print(id)
        url = "https://api.cloudflare.com/client/v4/zones/" + id + "/firewall/access_rules/rules"
        data = {"mode":mode,"configuration":{"target":"ip","value":ip},"notes":notes}
        data= json.dumps(data)
        data1 = str(data)
        req = requests.post(url,data=data1,headers=val)
        return req.json()

        # 列出指定域名下面指定ip的防护墙规则的ID
    def list_domain_Rules_id(self, ip, domain):
        dict01 = {}
        rules_id = []
        for i in self.List_domain_Access_Rules(domain):
            key = i['configuration']['value']
            value = i['id']
            dict01.setdefault(key, value)
        if ip in dict01.keys():
            rules_id.append(dict01[ip])
        else:
            exit("该域名下面不存在这个IP的防火墙规则的ID")
        return rules_id[0]
    #删除域名下面的防火墙规则
    def del_domain_Rules(self,domain,ip):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        id = self.chice_zone_id(domain)
        rule_id=self.list_domain_Rules_id(ip,domain)
        url = "https://api.cloudflare.com/client/v4/zones/" + id + "/firewall/access_rules/rules/" + rule_id
        data = {"cascade":"none"}
        data = json.dumps(data)
        data1 = str(data)
        req = requests.delete(url, data=data1, headers=val)
        return req.json()
    #给账户下面添加防火墙规则
    def add_account_Rules(self,ip,mode,notes):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        id = self.list_accounts()['id']
        url = "https://api.cloudflare.com/client/v4/accounts/" + id + "/firewall/access_rules/rules"
        data = {"mode": mode, "configuration": {"target": "ip", "value": ip}, "notes": notes}
        data = json.dumps(data)
        data1 = str(data)
        req = requests.post(url, data=data1, headers=val)
        return req.json()

    #列出全局账户下面指定IP的防火墙规则ID
    def list_account_Rules_id(self,ip):
        dict01 = {}
        rules_id = []
        for i in self.list_account_Rules():
            key = i['configuration']['value']
            value = i['id']
            dict01.setdefault(key, value)
        if ip in dict01.keys():
            rules_id.append(dict01[ip])
            print(dict01[ip])
        else:
            exit("全局账户不存在这个IP的防火墙规则")
        return rules_id[0]
    #删除账户下面全局防火墙规则
    def del_account_Rules(self,ip):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        id = self.list_accounts()['id']
        rule_id = self.list_account_Rules_id(ip)
        url = "https://api.cloudflare.com/client/v4/accounts/" + id + "/firewall/access_rules/rules/" + rule_id
        req = requests.delete(url, headers=val)
        return req.json()

    #列出用户账号的细节
    def list_user(self):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type,'X-Auth-User-Service-Key': self.user_service_api_key}
        url = "https://api.cloudflare.com/client/v4/user"
        req = requests.get(url, headers=val)
        return req.json()['result']

    ###在一个域名下面添加全局的防火墙规则
    def add_domain_Rules_to_all_zone(self,domain,ip,mode,notes):
        val = {'X-Auth-Email': self.Email, 'X-Auth-Key': self.auth_api_key, 'Content-Type': self.content_type, 'X-Auth-User-Service-Key': self.user_service_api_key}
        id =''
        if self.add_domain_Rules(domain,ip,mode,notes)['result']['success'] == True:
            id = self.list_domain_Rules_id(ip,domain)
        else:
            exit("单个域名的防火墙规则添加失败")
        url ='https://api.cloudflare.com/client/v4/user/firewall/access_rules/rules/' + id
        data = {"mode": mode,"notes": notes}
        data = json.dumps(data)
        data1 = str(data)
        req = requests.patch(url,data=data1,headers=val)
        return req.json()


if __name__ == '__main__':
    c = cloudflare()
    # print(c.get_zone_id())
    # for i in c.get_zone_id()['result']:
    #     print(i)
    #     print("域名对应的zone ID",i['id'],i['name'])
    #     for j in c.list_all_domain_record(i['name']):
    #         print("域名记录对应的record ID", j['id'], j['name'])
    # for i in c.list_all_domain_record('oppaier.com'):
    #     print(i)
    #print(c.Purge_Cache('855crown.com'))
    for i in (c.list_all_domain_record('w855.bet')):
        print(i)
    #w855.bet 192.168.30.3 A www1 True
    # print(c.add_domain_record('A','www2','192.168.0.1','w855.bet'))
    print(c.del_domain_record('w855.cc','www1.w855.cc'))