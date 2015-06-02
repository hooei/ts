#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author: luojianqiang@youmi.net
#
# 线上环境cronteb 配置如下
# crontab -e
# */1 * * * * python /app_path/crontab/save_channel_click.py

import sys
import urllib2,urllib

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    """ redis to db """
   # url = 'http://172.16.2.209:8007/crontab/resend_anwo'
    url='http://qiandeer.com/crontab/resend_anwo'
    req = urllib2.Request(url, urllib.urlencode({}))
    response = urllib2.urlopen(req)
    response.read()

if(__name__=='__main__'):
    try:
        main()
    except Exception as e:
        print
