#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib3
import urllib.request
import urllib.parse
import itertools
import time
import hashlib
import requests
import sys
import json
values = {"HOST":"","UID":"","SKEY":"","PRODUCT":""}
from jinja2 import Template
from jinja2 import PackageLoader,Environment,Template,FileSystemLoader
#md5加密
def get_str_md5(str):
    m = hashlib.md5()
    m.update(str.encode(encoding='UTF8'))
    return m.hexdigest()
class CDNBest_api(object):
    def __init__(self):
        self.public_values = values
        self.headers={'accept': '*/*', 'Content-Type': 'application/json'}
    ###############################获取token#####################################
    def get_token(self, site):
        head = self.headers
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url_token = "http://" + host + ':82/api/user/login/token'
        t = int(time.time())
        sign = get_str_md5(get_str_md5(str(uid) + skey) + str(t))
        dto = {"sign": sign, "time": t, "uid": uid, "vhost": site}
        req_token = requests.post(url_token, headers=head, data=json.dumps(dto))
        # print(req_token.json())
        # print(req_token.json()['code'])
        # print(req_token.json()['data']['sessionId'])
        if req_token.json()['code']!=200:
            print(site + "api获取token失败!!!")
            return 0
        else:
            return req_token.json()["data"]["sessionId"]
    #################/api/user/login/token获取token################################################

    def get_token_user(self):
        head = self.headers
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url_token = "http://" + host + ':82/api/user/login/token'
        t = int(time.time())
        sign = get_str_md5(get_str_md5(str(uid) + skey) + str(t))
        dto = {'uid': uid, 'time': t, 'skey': skey, 'sign': sign}
        req_token = requests.post(url_token, headers=head, data=json.dumps(dto))
        # print(req_token.json())
        # print(req_token.json()['code'])
        # print(req_token.json()['data']['sessionId'])
        if req_token.json()['code'] != 200:
            print( "user api获取token失败!!!")
            return 0
        else:
            return req_token.json()["data"]["sessionId"]

    ########################## # 添加站点
    def add_site(self, site):
        head=self.headers
        head['Cookie']='JSESSIONID='+self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ':82/api/user/vhost'
        values = {'name': site, 'pid': PRODUCT,'passwd': "123456"}
        req = requests.post(url,data=json.dumps(values), headers=head)
        return req.json()

############ 删除站点
    def del_site(self, site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ':82/api/user/vhost/' + site
        req = requests.delete(url, headers=head)
        return req.json()

###############################获取所有站点名称
    def get_sites(self):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ":82/api/user/vhost/pagelist?pageNum=1&pageSize=500"
        token = self.get_token_user()
        req = requests.get(url=url,headers=head)
        return req.json()
    # 设置站点状态，0–正常 1–暂停 2–审核 3–认证 4–加入黑名单 5–流量超标 9–信息非法   0, 1, 2, 4, 8, 16, 32, 64, 128
    def set_status_site(self, vhost, status):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ':82/api/user/vhost/status/'+ vhost + '/'+ status

        req=requests.put(url,headers=head)
        return req.json()

        ###################################获取站点信息 获取站点设置、防火墙设置的所有信息
    def get_site_info(self, site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ":82/api/site/"+ site + "/setting"
        # req_get(url,jdata)
        req = requests.get(url=url, headers=head)
        return req.json()
    ################获取站点的配置
    def get_site_config(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ":82/api/user/vhost/config?name=telnet&pageNum=1&pageSize=100&vhost=" + site
        req = requests.get(url=url, headers=head)
        return req.json()

###################################### 获取域名列表 ###############
    def get_domain_list(self, site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://"+host+":4430/api/site/" + site +"/domain/page?pageNum=1&pageSize=50"
        urllib3.disable_warnings()
        req=requests.get(url, headers=head, verify=False)
        return req.json()
###单个站点添加域名 ################################
    def add_domain(self,site,domain,ip):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url="https://18.163.221.20:4430/api/site/"+site+"/domain"
        dto={"domain":domain,"host":ip}
        urllib3.disable_warnings()
        req=requests.post(url,data=json.dumps(dto),headers=head,verify=False)
        return req.json()['message']
###########################################修改域名############################
    def modify_domain(self,site,domain,ip):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        domain_list = self.get_domain_list(site)
        flag = 0
        if domain_list["code"] == 200:
            for item in domain_list['data']['list']:
                if domain == item["domain"]:
                    flag = 1
                    domain_id = item["id"]
                    break
            if flag == 1:
                urllib3.disable_warnings()
                dto={"domain": domain, "host": ip,"weight": 1}
                url = "https://18.163.221.20:4430/api/site/"+site+"/domain/"+"/"+ str(domain_id)
                req=requests.put(url,data=json.dumps(dto),headers=head,verify=False)
                return req.json()

###############################################删除域名
    def delete_domain(self,site,domain):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        domain_list = self.get_domain_list(site)
        flag = 0
        if domain_list["code"] == 200:
            for item in domain_list['data']['list']:
                if domain == item["domain"]:
                    flag = 1
                    domain_id = item["id"]
                    break
            if flag == 1:
                urllib3.disable_warnings()
                url = "https://18.163.221.20:4430/api/site/" + site + "/domain/" + "/" + str(domain_id)
                req=requests.delete(url,headers=head,verify=False)
                return req.json()['message']

        #################################################开启站点长连接
    def set_site_lifetime(self, site, second):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/"+site+"/setting/lifetime"
        token = self.get_token(site)
        dto={"second":second}
        urllib3.disable_warnings()
        req = requests.post(url,data=json.dumps(dto),headers=head,verify=False)
        return req.json()
############################## 站点默认缓存设置
    def set_site_cachetime(self,site,second):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/"+site+"/setting/defaultcache"
        dto={"second":str(second)}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
########################################刷新缓存
    def flush_cache(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://"+host+":4430/api/site/" + site + "/setting/cacheflushtime"
        dto = {"hard": 1}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
###################################站点gzip设置
    def gzip_setting(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/" + site + "/setting/gzip"
        dto={"supportCss": True,"supportHtml": True,"supportJs": True}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
################################删除站点gzip设置
    def del_gzip_setting(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/" + site + "/setting/gzip"
        dto={"supportCss": False,"supportHtml": False,"supportJs": False}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
########################################域名添加重写
    def add_redirect(self,site,domain):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/"+site+"/setting/urlredirect"
        if len(domain.split(".")) == 2:
            dto = {"code": 301, "host": 'http://' + domain + '(.*)$', "target": 'https://www.' + domain +'$1'}
        else:
            dto = {"code": 301, "host": 'http://' + domain + '(.*)$', "target": 'https://' + domain +'$1'}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
#######################################域名删除重写
    def del_redirect(self,site,domain):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        redirect_settings = self.get_site_info(site)
        flag = 0
        for i in redirect_settings["data"]:
            if i["name"] == "redirect" and i['decodeValue']['host'].split('/')[2].split('(')[0] == domain:
                flag = 1
                domain_id = i['id']
                break
        if flag == 1:
            url = "https://18.163.221.20:4430/api/site/"+site+"/setting/urlredirect/"+str(domain_id)
            urllib3.disable_warnings()
            req = requests.delete(url, headers=head, verify=False)
            return req.json()
#################################### #判断域名是否已经添加重写 0为没有添加重写  | 1为已经添加重写
    def judge_domain_urlwrite(self,site,domain):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        redirect_settings = self.get_site_info(site)
        flag = 0
        for i in redirect_settings["data"]:
            if i["name"] == "redirect" and i['decodeValue']['host'].split('/')[2].split('(')[0] == domain:
                flag = 1
                #domain_id = i["id"]
                break
        return flag
######################################判断站点是否已经添加进证书
    def judge_ssl_certs(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url="https://18.163.221.20:4430/api/site/"+site+"/setting/https/check"
        urllib3.disable_warnings()
        req = requests.get(url, headers=head, verify=False)
        return req.json()
################################开启防cc设置,frcquency:medium,low,high; model:0,2,1
    def set_defend_cc(self,site,frcquency,model):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/"+site+"/setting/anticc"
        print(url)
        dto = {"frcquency": frcquency,"frequency": frcquency,"model": model}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()

    ################### 删除防CC设置
    def del_defend_cc(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://18.163.221.20:4430/api/site/" + site + "/setting/anticc"
        urllib3.disable_warnings()
        req=requests.delete(url,headers=head,verify=False)
        return req.json()

    ###############################判断是否有防cc设置 0 是没有 | 1 是有
    def judge_defend_cc(self, site):
        setting_firewall = self.get_site_info(site)
        flag = 0
        for i in setting_firewall["data"]:
            if i["name"] == "anticc":
                flag = 1
                break
        return flag

###############################访问频率设置
    def set_ipfrequency(self,site,time,second,exist_second):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        dto={"exist_second": exist_second, "second": second,"time": time, "type": 0}
        url="https://"+host +":4430/api/site/"+site+"/setting/ipfrequency"
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()


####################删除访问频率设置
    def del_ipfrequency(self, site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://"+host+":4430/api/site/" + site + "/setting/ipfrequency"
        urllib3.disable_warnings()
        req = requests.delete(url, headers=head, verify=False)
        return req.json()
########################判断访问频率设置是否已经添加
    def judge_ipfrequency(self,site):
        setting_firewall = self.get_site_info(site)
        flag = 0
        for i in setting_firewall["data"]:
            if i["name"] == "ipfrequency":
                flag = 1
                break
        return flag
##############站点图片压缩
    def set_site_webp(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://"+host+":4430/api/site/" + site + "/setting/webp"
        dto={"pictureSuffix": "gif|jpeg|jpg|png", "quality": 7}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
#################防火墙设置之白名单IP ip集合，格式127.0.0.1|127.0.0.2|127.0.0.2,每个ip使用|分割
    def whiteip_add(self,site,ips):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://" + host + ":4430/api/site/" + site + "/setting/whiteip"
        dto={"ips": ips}
        urllib3.disable_warnings()
        req = requests.post(url, data=json.dumps(dto), headers=head, verify=False)
        return req.json()
    def whiteip_del(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "https://" + host + ":4430/api/site/" + site + "/setting/whiteip"
        urllib3.disable_warnings()
        req = requests.delete(url, headers=head, verify=False)
        return req.json()
##################
    '''
    jump_type*	integer($int32)目标，0：接受|1：拒绝|7：继续
    id*	integer($int32) example: 1 编号
    name string 模块名称，url:url模块|meth:方法模块|referer:来源模块|user-agent：user agent模块|rewrite,redirect：url重写模块|srcs：srcs模块|host：代理模块|file_ext：文件后缀
    or [ url, meth, referer, user-agent, redirect, srcs, host, path_sign, header_mapper ] integer($int32) example: 1 or，0:否|1：是
    revers integer($int32) example: 1 非，0:否|1：是
    value*	{description:	模块中的内容< * >:	string }
    '''
    def Firewall_advanced(self,site,jump_type,id,name,oor,revers,additionalProp1,id2,name2,oor2,revers2,additionalProp2):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        dto={"jump_type": jump_type,
             "rules": [
                       {"id": id, "name": name, "or": oor, "revers": revers, "value": {name: additionalProp1}},
                       {"id": id2, "name": name2, "or": oor2, "revers": revers2, "value": {name2: additionalProp2}}
                      ]
             }
        url = "http://" + host + ":82/api/site/" + site + "/setting/advanced"
        urllib3.disable_warnings()
        req = requests.post(url, headers=head, verify=False,data=json.dumps(dto))
        return req.json()

#防火墙设置之防xss开关

    def set_defend_httponly(self,site):
         head = self.headers
         head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
         uid = self.public_values["UID"]
         PRODUCT = self.public_values["PRODUCT"]
         host = self.public_values["HOST"]
         skey = self.public_values["SKEY"]
         url = "http://" + host + ':82/api/site/'+site+'/setting/httponly'
         dto={"cookie": 1}
         req = requests.post(url, headers=head,data=json.dumps(dto))
         return req.json()
    def del_defend_httponly(self,site):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ':82/api/site/' + site + '/setting/httponly'
        req = requests.delete(url, headers=head)
        return req.json()

    def set_site_error(self, site, code, mem):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        dto={"mem": mem,"type": 0,"vhost": site}
        url = "http://" + host + ':82/api/site/' + site + '/error/' +code
        req = requests.put(url, headers=head, data=json.dumps(dto))
        return req.json()
    def nodelist(self,ngid):
        head = self.headers
        head['Cookie'] = 'JSESSIONID=' + self.get_token_user()
        uid = self.public_values["UID"]
        PRODUCT = self.public_values["PRODUCT"]
        host = self.public_values["HOST"]
        skey = self.public_values["SKEY"]
        url = "http://" + host + ':82//api/user/node'
        dto = {"ngid": ngid}
        req = requests.get(url, headers=head, data=json.dumps(dto))
        return req.json()['data']

if __name__ == '__main__':
    c=CDNBest_api()
    # print(c.add_site("qqq"))
    # print(c.del_site('qqq'))
    #print(c.get_sites()['data']['list'])
    #站点维护
    ###############################################################
    # print(c.set_status_site('bailin','1'))
    # env=Environment(loader=FileSystemLoader('', 'utf-8'))
    # template=env.get_template('index-templates.html')
    # indexhtml = template.render(logo_url="", customer_service_url="#", phone_num="400-120-0000", begin_time="2020/09/07 09:00(GMT+8)", end_time="2020/09/07 12:00(GMT+8)")
    # print(c.set_site_error('bailin','503',indexhtml))
    ###############################################################
    # 获取所有站点的信息
    for i in c.get_sites()['data']['list']:
       print(i['name'])
    #获取站点设置、防火墙设置的所有信息
    #print(c.get_site_info('ttt'))
    # print(c.get_site_config('ttt'))
    # for i in c.get_domain_list('ttt')['data']['list']:
    #     print(i)
    ##站点添加域名
    #print(c.add_domain('ttt','www.123.com','127.0.0.1:80'))
    # ##站点修改域名
    #print(c.modify_domain('ttt','www.123.com','1.1.1.1:80'))
    # ##站点删除域名
    #print(c.delete_domain('ttt','www.123.com'))
    # for i in c.get_domain_list('ttt')['data']['list']:
    #     print(i['domain'], "  ",i['host'],  i['id'])
    # ##站点删除域名
    # print(c.delete_domain('ttt','www.123.com'))
    #开启站点的长连接
    #print(c.set_site_lifetime('ttt',9))
    #站点设置缓存时间
    #print(c.set_site_cachetime('ttt',3600))
    #站点刷新缓存
    #print(c.flush_cache('dg'))
    #站点压缩的设置
    #print(c.gzip_setting('ttt'))
    #添加域名的重写
    #print(c.add_redirect('ttt','www.123.com'))
####删除域名重写
    # print(c.del_redirect('ttt','www.123.com'))
    ##判断域名是否添加重写
    # print(c.judge_domain_urlwrite('ttt','www.baidu.com'))
    # print(c.judge_domain_urlwrite('ttt', 'www.123.com'))
    # for i in c.get_site_info('ttt')['data']:
    #     print(i)
###判断站点是否添加证书
    # print(c.judge_ssl_certs('dgnew'))
    #站点防CC设置
    #print(c.set_defend_cc('ttt','high',1))
    #
    # for i in c.get_site_info('ttt')['data']:
    #     print(i['name'])
    # #站点删除防CC设置
    #print(c.del_defend_cc('ttt'))
    # for i in c.get_site_info('ttt')['data']:
    #     print(i['name'])

    #判断站点是否有防CC设置
    #print(c.judge_defend_cc('dg'))
    # 访问频率的设置
    #print(c.set_ipfrequency('ttt', 5000, 2, 3600))
    # print(c.judge_ipfrequency('ttt'))
    # #删除访问频率的设置
    #print(c.del_ipfrequency('ttt'))
    #print(c.judge_ipfrequency('king855'))

    #print(c.whiteip_add('ttt','172.16.30.30|192.168.60.100|192.168.100.10'))
    #print(c.whiteip_del('ttt'))

#防火墙设置之防xss开关
    #print(c.set_defend_httponly('king855-test'))
    #print(c.del_defend_httponly('king855-test'))
    #######获取节点信息
    # for i in c.nodelist(511):
    #     print(i)


