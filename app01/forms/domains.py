#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
class domainModelForm(forms.Form):
      name = forms.CharField(label='添加cloudfare的域名')