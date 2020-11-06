#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
#from django.urls import RegexURLResolver, RegexURLPattern
from django.urls.resolvers import URLResolver,URLPattern


def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取url
    :param pre_namespace: namespace 前缀 以后用于拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有的url
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发 添加到字典url_ordered_dict中
            if not item.name:
                continue
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name

            url = pre_url + str(item.pattern)  #
            url = url.replace("^", "").replace("$", "")
            if check_url_exclude(url):  # 判断是否admin、login等我们不需要的url，是的话直接跳过
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):  # 路由分发， 继续递归
            if pre_namespace:
                if item.namespace:
                    namespace = f"{pre_namespace}:{item.namespace}"
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None  # 父级没有namespace，自己也没有
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)  # from luff.. import urls
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict
