#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from rbac.service.urls import memory_reverse
from app01.domainapi.cash855_cloudflare_api import cloudflare
from app01.domainapi.cash855_godaddy_api import Godaddy_API
from app01.forms.domains import domainModelForm
from app01.domainapi.CDNBEST_NEW import CDNBest_api

def gdomains_list(request):
    gdomains_list = Godaddy_API().list_all_domains()
    return render(request, 'domains_list.html', {"gdomains_list": gdomains_list})

def cloudfare_list(request):
    cloudflare_list_domain = cloudflare().get_zone_id()['result']
    domain = request.GET.get('domain')
    if domain is None:
        cloudflare_domain_record=[]
    if domain:
        cloudflare_domain_record=cloudflare().list_all_domain_record(domain)
    response = {"dm": None, "msg": None}
    if request.method == 'POST':
        domain1 = request.POST.get('dm')
        d_ip=request.POST.get('dm_ip')
        d_type=request.POST.get('dm_ty')
        d_rd = request.POST.get('dm_rd')
        print(d_type,d_rd,d_ip,domain1)
        del_dm = request.POST.get('del_dm')
        del_dm_rd = request.POST.get('del_dm_rd')
        print(del_dm, del_dm_rd)
        try:
            d1 = cloudflare().add_domain_record(d_type,d_rd,d_ip,domain1)
            if d1['success'] is True:
                response['dm'] = domain1
                response['msg'] = '添加域名成功'
                return JsonResponse(response)
            else:
                response['msg'] = '添加域名失败'
                return JsonResponse(response)
        except SystemExit as e:
            print('添加的域名为空')
        try:
            d2 = cloudflare().del_domain_record(del_dm, del_dm_rd)
            if d2['success'] is True:
                response['dm'] = domain1
                response['msg'] = '删除域名成功'
                return JsonResponse(response)
            else:
                response['msg'] = '删除域名失败'
                return JsonResponse(response)
        except SystemExit as e:
             print('删除的域名为空')
    return render(request, 'cloudfare_list.html', {"cloudflare_list_domain": cloudflare_list_domain,'cloudflare_domain_record':cloudflare_domain_record})
def cf_domian_add(request):
    '''

    :return:
    '''
    if request.method == 'GET':
        form = domainModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = domainModelForm(data=request.POST)
    if form.is_valid():
        domain=form.data['name']
        add_domain=cloudflare().create_domain_zone(domain)
        return redirect(memory_reverse(request, 'cloudfare_list'))
    return render(request, 'rbac/change.html', {'form': form})
if __name__ == '__main__':
    c= cloudflare()
    print(c.get_zone_id())

