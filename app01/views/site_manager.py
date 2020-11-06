#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from rbac.service.urls import memory_reverse
from app01.domainapi.cash855_cloudflare_api import cloudflare
from app01.domainapi.cash855_godaddy_api import Godaddy_API
from app01.domainapi.CDNBEST_NEW import CDNBest_api

def site_list(request):
    '''
    :return:
    '''

    siteList = []
    for i in CDNBest_api().get_sites()['data']['list']:
        siteList.append(i['name'])
    sitetest = request.GET.get('dropdown')
    print(sitetest)
    return render(request, 'site_list.html', {'siteList': siteList})