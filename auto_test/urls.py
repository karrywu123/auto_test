"""auto_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from app01.views import user
from app01.views import host
from app01.views import account
from app01.views import domainset,site_manager

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^rbac/', include(('rbac.urls','rbac'),namespace='rbac')),
    url(r'^login/$', account.login, name='login'),
    url(r'^logout/$', account.logout, name='logout'),

    url(r'^index/$', account.index, name='index'),

    url(r'^user/list/$', user.user_list, name='user_list'),
    url(r'^user/add/$', user.user_add, name='user_add'),
    url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

    url(r'^host/list/$', host.host_list, name='host_list'),
    url(r'^host/add/$', host.host_add, name='host_add'),
    url(r'^host/edit/(?P<pk>\d+)/$', host.host_edit, name='host_edit'),
    url(r'^host/del/(?P<pk>\d+)/$', host.host_del, name='host_del'),

    url(r'^domain/godaddy_list/$',domainset.gdomains_list,name="godaddy_list"),
    url(r'^domain/cloudfare_list/$',domainset.cloudfare_list,name='cloudfare_list'),
    #cf_domian_add
    url(r'^domain/cf_domian_add/$',domainset.cf_domian_add,name='cf_domian_add'),

    url(r'^site/list/$',site_manager.site_list,name='site_list'),

]
