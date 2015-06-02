#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: luojianqiang@youmi.net
#
# 线上环境cronteb 配置如下
# crontab -e
# 58 * * * * python /app_path/crontab/save_channel_click.py

import sys
import urllib2,urllib

reload(sys)
sys.setdefaultencoding('utf-8')

def save():
    """ redis to db """
    #url = 'http://172.16.11.235:8007/crontab/save_channel_click'
    url='http://qiandeer.com/crontab/save_channel_click'
    req = urllib2.Request(url, urllib.urlencode({}))
    response = urllib2.urlopen(req)
    response.read()

if(__name__=='__main__'):
    try:
        save()
    except Exception as e:
        print e
