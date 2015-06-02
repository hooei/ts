#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""邀请相关

"""

import tornado.web
import utils
import urlparse
import time
import urllib
from datetime import datetime, date
from protocols import WebBaseHandler
from models import invites, options, users,activity, rule


class MyInviteHandler(WebBaseHandler):
    """ 我的邀请 """

    @tornado.web.authenticated
    def get(self):
        # 今日邀请
        today = date.today().strftime("%Y%m%d")
        iv_today = invites.get_invite(self.current_user['uid'], today)
        rate = options.get('rate')
        invite_earn = "%.2f" % (self.current_user['iv_points'] / float(rate))
        # FIXME 改成后台设置
        act_data = activity.get("hao")
        endtime = time.mktime(time.strptime(str(act_data['end_time']),'%Y-%m-%d %H:%M:%S'))
        #enddate = date(2015,04,10)
        #endtime = time.mktime(enddate.timetuple())
        activeTime = (endtime - time.time())*1000
        if activeTime <= 0:
            activeTime = 0
        #+ datetime.timetuple(days=7)
        #用户等级
        user_info = users.get_info(self.current_user['uid'])
        level = user_info['grade']
        value = rule.get(level)
        data = {
            "today_son": iv_today['sons'] if iv_today else 0,
            "total_son": self.current_user['sons'],
            "today_grandson": iv_today['grandsons'] if iv_today else 0,
            "total_grandson": self.current_user['grandsons'],
            "invite_earn": invite_earn,
            "uid": self.current_user['uid'],
            "activeTime": activeTime,
            "value" : value
        }
        base_url = self.config['url']['base']
        # uid 对应4位邀请码
        scode = utils.base34.encode(self.current_user['uid'])
        share = urllib.quote(urlparse.urljoin(base_url, 'share?scode=%s&cne=%s' % (scode, user_info['pkg'])))
        url = {
            "share": share,
        }
        return self.render("prentice/prentice.html", data=data, url=url)


class ShareHandler(WebBaseHandler):
    """ 分享页面 """

    def get(self):
        try:
            scode = self.get_argument('scode', '')
            cne = self.get_argument('cne','')
            uid = utils.base34.decode(str(scode))
            user_info = users.get_info(uid)
            if not user_info:
                raise Exception
            if user_info['username'] == None:
                user_info['username'] = ''
        except:
            return self.redirect("/welcome")
        base_url = self.config['url']['base']
        data = {
            "uid": user_info['tid'],
            "username": user_info['username'],
            "days": self._get_days(user_info['create_time']),
            "url": urllib.quote(urlparse.urljoin(base_url, 'welcome?scode=%s&cne=%s' % (scode, cne)))
        }
        ios = self.get_argument('ios', 0)
        if ios:
            self.render("prentice/share-ios.html", data=data)
        else:
            self.render("prentice/share.html", data=data)


    def _get_days(self, create_time):
        """ 考虑用户信息redis缓存后时间的问题 """
        if isinstance(create_time, int):
            d = datetime.utcfromtimestamp(create_time)
        elif isinstance(create_time, datetime):
            d = create_time
        else:
            log_path = self.config['log']['error']
            utils.loggers.use('error', log_path).info(create_time)
            return 0
        return ((datetime.now() - d ).days + 1)


class DownloadHandler(WebBaseHandler):
    def get(self):
        url = options.get_url()
        url = "itms-services://?action=download-manifest&url=" + url
        # self.redirect("itms-services://?action=download-manifest&url=https://ym-au.b0.upaiyun.com/app/qd/ios/1430965793944/qd.plist")
        self.redirect(url)


class CardHandler(WebBaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_info = users.get_info(self.current_user['uid'])
        base_url = self.config['url']['base']
        # uid 对应4位邀请码
        scode = utils.base34.encode(self.current_user['uid'])
        url = urllib.quote(urlparse.urljoin(base_url, 'share?scode=%s&cne=%s' % (scode, user_info['pkg'])))
        data = {
            'name': user_info['username'] if user_info['username'] else '',
            'id': user_info['tid'],
            'siu': user_info['headimg'] if user_info['headimg'] else '',
            'url': url
        }
        self.render('prentice/card.html', data=data)
