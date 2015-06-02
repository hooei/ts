#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""用户信息相关

"""
import struct
import xlrd
import os
import tornado.web
import tornado.escape
import urlparse
import urllib, urllib2
import time
import random
import base64
import constants
import utils
import ujson as json
import IP
from tornado import httpclient
from PIL import Image
from datetime import date, datetime, timedelta
from crypt import AESCipher
from protocols import WebBaseHandler
from models import users, orders, invites, options,activity, rule, wallad_clicks, channel, task
from modules import captcha, level
from Crypto.Cipher import AES

class WelcomeHandler(WebBaseHandler):
    """ 登陆页面 """

    def get(self):
        # 跳转服务器维护页面
        #return self.render("error/error_fix.html")
        ua = self.request.headers["User-Agent"]
        platform = utils.get_platform(ua)
        if platform == 0:
            return self.render("pc.html")
        # print self.current_user
        # print self.session.session_id, self.session
        # 检查版本号
        av = options.get('av')
        download_url = options.get_url()
        '''
        if av > int(self.session.get('av', av)):
            print `av` + av
            self.redis.delete(self.session.session_id)
            data = {
                "ssid": self.session.session_id,
                "aurl": self.config['url']['base'],
                # FIXME 添加后台设置
                "appUrl": urllib.quote(download_url),

            }
            return self.render("update.html", data=data)
        '''
        # 判断用户是否登陆成功
        if self.current_user:
            return self.redirect('/home')
        scode = self.get_argument('scode', None)
        cne = self.get_argument('cne', '0')
        data = {
            "ssid" : self.session.session_id,
            "scode": scode,
            "cne"  : cne,
            "ex"   : [{'test':'test'}],
            "aurl" : self.config['url']['base'],
            # FIXME 添加后台设置
            "appUrl": urllib.quote(download_url),
            "av": av
        }
        ip = self.request.remote_ip
        user_log = self.config['log']['user']
        utils.loggers.use('user', user_log).info(`self.request.headers`+'&ip='+`ip`+'&ssid='+`self.session.session_id`)

        #排行榜显示
        today = date.today()
        now = int(time.time())
        tomorrow = today + timedelta(days=1)
        edate = int(time.mktime(time.strptime(str(tomorrow),"%Y-%m-%d")))
        expire = edate - now
        print expire
        file_dir = 'static/list_data.xlsx'
        info = xlrd.open_workbook(file_dir)
        table = info.sheets()[1]
        rank = {}
        rank['info'] = []
        for r in range(table.nrows)[1:9]:
            d = table.row_values(r)
            name = d[0]
            img = d[1]
            value = self.redis.get("qianka:rank:"+name)
            #self.redis.setex("qianka:rank:"+name,round(random.uniform(400, 500),2),expire)
            if not value:
                self.redis.setex("qianka:rank:"+name,round(random.uniform(400, 500),2),expire)
            rank['info'].append({
                'name' : name,
                'img'  : img,
                'earn' : self.redis.get("qianka:rank:"+name)
            })
        rank['info'].sort(lambda x,y: cmp(x['earn'],y['earn']))
        rank['info'] = sorted(rank['info'],key=lambda x:x['earn'])
        rank['top'] = []
        table = info.sheets()[0]
        for r in range(table.nrows)[1:]:
            d = table.row_values(r)
            name = d[0]
            img = d[1]
            earn = d[2]
            value = self.redis.get("qianka:rank:"+name)
            #self.redis.setex("qianka:rank:"+name,earn + round(random.uniform(400, 500),2),expire)
            if not value:
                self.redis.setex("qianka:rank:"+name, earn + round(random.uniform(200 ,300),2),expire)
            money = float(self.redis.get("qianka:rank:"+name))
            rank['top'].append({
                'name': name,
                'img': img,
                'earn': "%.2f" % money
            })
        rank['deal'] = []
        nickname = []
        table = info.sheets()[2]
        for r in range(table.nrows)[1:]:
            d = table.row_values(r)
            nickname.append(d[0])
        way = ['支付宝提款','Q币充值','手机充值']
        money = ['10','20','30','50']
        random.shuffle(nickname)
        random.shuffle(way)
        random.shuffle(money)
        for i in range(0,10):
            rank['deal'].append({
                'name' : nickname[i],
                'desc' : "通过"+way[random.randint(0,2)]+" 成功提款"+money[random.randint(0,3)]+"元",
                'time' : str(random.randint(1,20)) + "分钟前"
            })

        self.render('login.html', data=data, rank=rank)


class IsLoginHandler(WebBaseHandler):
    """ 检查用户是否已登陆成功 """

    def get(self):
        if self.current_user:
            return self.return_success()
        else:
            return self.return_error(constants.ERR_NO_LOGIN)


class HomeHandler(WebBaseHandler):
    """ 用户首页 """

    @tornado.web.authenticated
    def get(self):
        users.set_last_login(self.current_user['uid'], datetime.now())
        if not self.current_user['platform']:
            users.set_platform(self.current_user['uid'], self.platform)
        ip = self.request.remote_ip
        if not users.get_user_ip(self.current_user['uid'], ip):
            users.set_user_ip(ip, self.current_user['uid'], IP.find(ip))

        invite_by = self.get_argument('uid', None)
        pack = self.get_argument('pack', None)
        data = self._get_data(self.current_user['uid'], invite_by, pack)
        act_data = activity.get("vip")
        endtime = time.mktime(time.strptime(str(act_data['end_time']),'%Y-%m-%d %H:%M:%S'))
        activeTime = (endtime - time.time())*1000
        if activeTime <= 0:
            activeTime = 0
        url = self._get_url()
        #等级读取
        level.get_level(self.current_user['uid'])
        #js等级效果
        r = self.redis.hget("qianka:showpoint",self.current_user['uid'])
        if not r:
            self.redis.hset("qianka:showpoint",self.current_user['uid'],1)
            showpoint = 1
        else:
            showpoint = 0
        return self.render("home.html", url=url, activeTime=activeTime, data=data, showpoint=showpoint)

    def _get_data(self, uid, invite_by, pack):
        """ 页面数据 """
        # 今日赚取
        today = date.today().strftime("%Y%m%d")
        # 是否首次登陆
        first = self.session.get('first', 0)
        # 新手红包
        parent = users.get_info_bytid(invite_by)
        newmoney = 0
        rate = int(options.get('rate'))
        gift = orders.get_otype_orders(uid, 4)
        inputFail = 0
        if gift:
            bound = 0
        else:
            bound =1
        login_log = self.config['log']['bound']
        utils.loggers.use('login', login_log).info(
            "tid:"+str(self.current_user['tid'])\
            +" invite:"+str(invite_by)+" pack:"+str(pack)\
            +" bound:"+str(bound)+" gift:"+str(gift)
        )

        if bound == 1 and (not gift) and pack == '1':
            if parent and (str(invite_by) != str(self.current_user['tid'])) \
                    and (invite_by != ''):
                # 师徒关系只允许在同一平台之内
                if parent['platform'] == self.current_user['platform'] and self.current_user['platform'] !=0 :
                    # 有uid加3元
                    bonus = 3
#                     utils.loggers.use('login', login_log).info("tid:"+str(self.current_user['tid'])+" money:"+str(bonus) +" invite:"+str(invite_by)+"ready:ok")
                    utils.loggers.use('login', login_log).info("tid:%s money:%s invite:%s ready:ok"  % (self.current_user['tid'], bonus, invite_by))
                    users.add_tt_points(self.current_user['uid'], bonus*rate)
                    orders.new_global_order(self.current_user['uid'], self.current_user['points'], bonus*rate, 4, u'新手红包')
                    users.set_bonus(self.current_user['uid'], bonus)    #标记用户的奖励为2元，方便结算时数据统计；
                    
                    ad_kidd=u'恭喜您成功收获了一名徒弟！'
                    orders.new_global_order(parent['uid'], parent['points'], 0, 2, ad_kidd)
                    # 一级邀请
                    users.set_invite(uid, parent['uid'], parent['parent'])
                    self._add_invite(parent['uid'], son=1)
                    # 判断二级邀请
                    if parent['parent']:
                        grandfather = users.get_info(parent['parent'])
                        ad_son=u'恭喜您成功收获了一名徒孙！'
                        orders.new_global_order(parent['parent'], grandfather['points'], 0, 2, ad_son)
                        self._add_invite(parent['parent'], grandson=1)
#                     utils.loggers.use('login', login_log).info("tid:"+str(self.current_user['tid'])+" money:"+str(bonus)+" invite:"+str(invite_by))
                    utils.loggers.use('login', login_log).info("tid:%s money:%s invite:%s"  %  (self.current_user['tid'], bonus, invite_by))
                    bound = 0
                    inputFail = 0
                    self.youmi()
                else:
                    inputFail = 1
            if (not parent) or (invite_by == str(self.current_user['tid'])):
                utils.loggers.use('login', login_log).info(
                    "tid:"+str(self.current_user['tid'])+\
                    " invite:"+str(invite_by)+"error: invild invite_code")
                inputFail = 1

            if invite_by == '':
                # 无uid加2元
                bonus = 2
#                 utils.loggers.use('login', login_log).info("tid:"+str(self.current_user['tid'])+" money:"+str(bonus)+"ready:ok" )
                utils.loggers.use('login', login_log).info("tid:%s money:%s ready:ok"  % (self.current_user['tid'], bonus) )
                users.add_tt_points(self.current_user['uid'], bonus*rate)
                orders.new_global_order(self.current_user['uid'], self.current_user['points'], bonus*rate, 4, u'新手红包')
                users.set_bonus(self.current_user['uid'], bonus)    #标记用户的奖励为2元，方便结算时数据统计；
#                 utils.loggers.use('login', login_log).info("tid:"+str(self.current_user['tid'])+" money:"+str(bonus)+" invite:"+str(invite_by))
                utils.loggers.use('login', login_log).info("tid:%s money:%s invite:%s"  %  (self.current_user['tid'], bonus, invite_by))
                bound = 0
                self.youmi()
        key_name = "qianka:earn:%s:%s" % (uid, today)
        data = self.redis.get(key_name)
        today_earn = "%.2f" % (float(data) if data else 0 )
        # 今日邀请
        iv_count = invites.get_invite(uid, today)
        today_invite = iv_count['sons'] + iv_count['grandsons'] if iv_count else 0
        # 我的余额
        money = "%.2f" % (users.get_info(self.current_user['uid'])['points'] / float(rate))
        # 累计统计
        user_stat= users.count_users()
        total_user = user_stat['dcount'] if user_stat['dcount'] else 0
        total_son = int(user_stat['dsum']) if user_stat['dsum'] else 0
        total_exchange = orders.count_exchange()
        # session的保存有问题,临时处理 FIXME
        s = {
            "oid": self.session.get('oid', ''),
            "ifa": self.session.get('ifa', ''),
            "av": self.session.get('av', ''),
            "first": 0,
        }
        self.redis.setex(self.session.session_id, json.dumps(s), 86400)
        number = int(time.time()) - 1422000000
        key_name = "qianka:scode:%s" % self.current_user['uid']
        dscode = self.redis.get(key_name)
        if dscode:
            bound = 0
            newmoney = 3
            self.redis.delete(key_name)

        #流量领取活动
        #user_info = users.get_info(self.current_user['uid'])
        if int(self.current_user['pkg']) == 5 and int(self.current_user['flow']) == 1 and bound == 0:
            count = users.summary_flow()
            if int(count['total']) >=5500:
                showFlow = 2
                users.flow_user(self.current_user['uid'], 0)
            else:
                showFlow = 1

        else:
            showFlow = 0
        data = {
            "headimg": self.current_user['headimg'],
            "username": self.current_user['username'],
            "tid": self.current_user['tid'],
            "invite": today_invite,
            "earn": today_earn,
            "money": money,
            "total_users": total_user+number/10,
            "total_sons": int(total_son)+number/30,
            "total_exchange": int(total_exchange+1)+number,
            "first": first,
            "bound": bound,
            "newmoney": newmoney,
            "inputFail": inputFail,
            "showflow" : showFlow #showFlow
        }
        return data

    def youmi(self):
        device = users.get_device_byuid(self.current_user['uid'])
        if len(device) == 1:
            adinfo = wallad_clicks.get_ifa(device[0]['ifa'])
            if adinfo:
                #添加IP防刷，由后台控制开关
                c = channel.get_by_id(adinfo['adserver'])
                if int(c['status']) == 1:
                    count = users.get_count_byip(self.current_user['ip'])
                    if int(count['total']) == 1:
                        callback_url = adinfo['callback_url']
                        try:
                            msg = str(urllib2.urlopen(callback_url).read())
                        except urllib2.HTTPError,e:
                            msg = str(e.code)
                        except urllib2.URLError,e:
                            msg = str(e)
                        self.db.execute(
                            "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s \
                            WHERE `id`=%s", self.current_user['uid'], msg, adinfo['id'])
                        wallad_clicks.set_user_pkg(self.current_user['uid'], adinfo['adserver'])
                else:
                    callback_url = adinfo['callback_url']
                    try:
                        msg = str(urllib2.urlopen(callback_url).read())
                    except urllib2.HTTPError,e:
                        msg = str(e.code)
                    except urllib2.URLError,e:
                        msg = str(e)
                    self.db.execute(
                        "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s \
                        WHERE `id`=%s", self.current_user['uid'], msg, adinfo['id'])
                    wallad_clicks.set_user_pkg(self.current_user['uid'], adinfo['adserver'])


    def _get_url(self):
        """ 跳转链接 """
        base_url = self.config['url']['base']
        url = {
            #"earn": self._encrypt_r(),
            "earn": urlparse.urljoin(base_url, 'task'),
            "invite": urlparse.urljoin(base_url, 'invite'),
            "exchange": urlparse.urljoin(base_url, 'exchange'),
            "detail": urlparse.urljoin(base_url, 'detail'),
            "config": urlparse.urljoin(base_url, 'config'),
            "level" : urlparse.urljoin(base_url,'level')
        }
        return url

    def _encrypt_r(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        key = self.config['ymsecret'][platform]
        appid = self.config['ymappid'][platform]
        aes = AESCipher(key)
        # 请求广告用ifa
        # s = '%s&%s' % (base64.b64encode(self.current_user['oid']),
        s = '%s&%s' % (base64.b64encode(self.session.get('ifa','')),
                       base64.b64encode(str(self.current_user['uid'])))
        # print self.current_user['oid']
        # print 'oid'
        # print self.session.get('ifa','')
        # print 'idfa---------------------------------'
        r = urllib.quote_plus(appid + aes.encrypt(s))
        # url_earn = 'http://w.ymapp.com/wx/%s/lists.html?r=%s&mt=1&bk=1' % (platform, r)
        #url_earn = 'http://w.qiandeer.com/qd/task/lists.html?r=%s' % r
        url_earn = 'http://w.qiandeer.com/qd/%s/lists.html?r=%s' % ('task', r)
        # url_earn = 'http://au.youmi.net/wx/%s/lists.html?r=%s' % (platform, r)
        # url_earn = 'http://au.ymapp.com/wx/%s/lists.html?r=%s' % (platform, r)
        # url_earn = 'http://au.youmi.net/wx/%s/lists.html?r=%s&mt=1&bk=1' % (platform, r)
        return url_earn

    def _add_invite(self, uid, son=0, grandson=0):
        """增加邀请人数，记录"""
        users.add_invite(uid, son, grandson)
        today = date.today().strftime("%Y%m%d")
        if invites.get_invite(uid, today):
            invites.add_invite(uid, son, grandson)
        else:
            invites.new_invite(uid, son, grandson)

class LevelHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.write("id error")
        else:
            uid = self.current_user['uid']
            user_info = users.get_info(uid)
            rules = rule.get_all()
            data = {}
            data['level'] = user_info['grade']
            data['hadSon'] = user_info['sons']
            data['hadMoney'] = user_info['tt_points'] / 100
            data['hadGrandSon'] = user_info['grandsons']
            data['require'] = []

            for r in rules:
                data['require'].append({
                    'level' : r['level'],
                    'title' : r['title'],
                    'money' : r['points'] / 100,
                    'son'   : r['sons'],
                    'prize' : r['value']
                })
            self.render('prentice/level.html',data=data)

class TaskHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        key = self.config['ymsecret'][platform]
        appid = self.config['ymappid'][platform]
        aes = AESCipher(key)
        # 请求广告用ifa
        # s = '%s&%s' % (base64.b64encode(self.current_user['oid']),
        s = '%s&%s' % (base64.b64encode(self.session.get('ifa','')),
                       base64.b64encode(str(self.current_user['uid'])))
        # print self.current_user['oid']
        # print 'oid'
        # print self.session.get('ifa','')
        # print 'idfa---------------------------------'
        r = urllib.quote_plus(appid + aes.encrypt(s))
        # url_earn = urllib.quote('http://au.youmi.net/wx/%s/lists.html?r=%s' % (platform, r))
        #url_earn = urllib.quote('http://au.ymapp.com/wx/%s/lists.html?r=%s' % (platform, r))
        #url_earn = 'http://w.qiandeer.com/qd/task/lists.html?r=%s' % r
        url_earn = urllib.quote('http://w.qiandeer.com/qd/%s/lists.html?r=%s' % ('task', r))

        # 是否还有首次任务 (1还有新手任务)
        count = task.first_task_ios(self.current_user['uid'])
        if count['total'] == 3:
            first = 0
        else:
            first = 1
        self.render("task/task.html", url=url_earn, first=first)


# 联盟任务页面
class UnionHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        self.render("task/union.html")


# 新手任务页面
class TeachHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'
        result = task.check_task_ios(self.current_user['uid'], 1)
        if result['total'] != 0:
            info = 1
        else:
            info = 0
        result = task.check_task_ios(self.current_user['uid'], 2)
        if result['total'] != 0:
            video = 1
        else:
            video = 0
        result = task.check_task_ios(self.current_user['uid'], 3)
        if result['total'] != 0:
            survey = 1
        else:
            survey = 0

        self.render("task/teach.html", info=info, video=video, survey=survey)


# 新手任务视频任务页面
class TaskVideoHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        # uid 对应4位邀请码
        user_info = users.get_info(self.current_user['uid'])
        base_url = self.config['url']['base']
        scode = utils.base34.encode(self.current_user['uid'])
        share = urllib.quote(urlparse.urljoin(base_url, 'share?scode=%s&cne=%s' % (scode, user_info['pkg'])))

        result = task.check_task_ios(self.current_user['uid'], 2)
        if result['total'] == 0:
            info = 0
        else:
            info = 1
        data = {
            "uid": self.current_user['uid'],
            "share": share,
            "info" : info
        }
        self.render("task/video.html", data=data)

    @tornado.web.authenticated
    def post(self):
        # 处理观看完视频
        result = task.check_task_ios(self.current_user['uid'], 2)
        if result['total'] == 0:
            task.new_task_ios(self.current_user['uid'], 2)
            users.add_tt_points(self.current_user['uid'], 20)
            orders.new_global_order(self.current_user['uid'], self.current_user['points'], 20, 1, u'新手任务：视频')
            _today_earn(self, self.current_user['uid'], 20)
            return self.return_success()
# 新手任务问卷调查任务页面
class TaskSurveyHandler(WebBaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        # uid 对应4位邀请码
        user_info = users.get_info(self.current_user['uid'])
        base_url = self.config['url']['base']
        scode = utils.base34.encode(self.current_user['uid'])
        share = urllib.quote(urlparse.urljoin(base_url, 'share?scode=%s&cne=%s' % (scode, user_info['pkg'])))
        result = task.check_task_ios(self.current_user['uid'], 3)
        if result['total'] == 0:
            info = 0
        else:
            info = 1

        data = {
            "uid": self.current_user['uid'],
            "share": share,
            "info" : info
        }
        self.render("task/survey.html", data=data)

    @tornado.web.authenticated
    def post(self):
        result = task.check_task_ios(self.current_user['uid'], 3)
        if result['total'] == 0:
            task.new_task_ios(self.current_user['uid'], 3)
            users.add_tt_points(self.current_user['uid'], 20)
            orders.new_global_order(self.current_user['uid'], self.current_user['points'], 20, 1, u'新手任务：问答')
            _today_earn(self, self.current_user['uid'], 20)
            return self.return_success()



class DetailHandler(WebBaseHandler):
    """ 用户赚取明细 """

    @tornado.web.authenticated
    def get(self):
        all_orders = orders.get_global_orders(self.current_user['uid'])
        cb_orders = orders.get_otype_orders(self.current_user['uid'], orders.OTYPE_TASK)
        iv_orders = orders.get_otype_orders(self.current_user['uid'], orders.OTYPE_INVITE)
        ex_orders = orders.get_ex_orders(self.current_user['uid'])
        # rate = options.get('rate')
        data = {
            "all": self._parse_time(all_orders),
            "callback": self._parse_time(cb_orders),
            "invite": self._parse_time(iv_orders),
            "exchange": self._parse_ex_time(ex_orders),
            "earn_url": self._encrypt_r(),
            # "rate": rate
        }
        self.render("detail/detail.html", data=data)

    def _parse_time(self, data=[]):
        """ 缓存&数据库 record_time 类型统一 """
        result = []
        for d in data:
            if isinstance(d['record_time'], int):
                t = datetime.utcfromtimestamp(d['record_time']).strftime("%Y年%m月%d日 %H:%M")
            elif isinstance(d['record_time'], datetime):
                t = d['record_time'].strftime("%Y年%m月%d日 %H:%M")
            else:
                t = d['record_time']
            rec = d
            rec['record_time'] = t
            result.append(rec)
        return result

    def _parse_ex_time(self, data=[]):
        """ 缓存&数据库 create_time 类型统一 """
        result = []
        for d in data:
            if isinstance(d['create_time'], int):
                t = datetime.utcfromtimestamp(d['create_time']).strftime("%Y年%m月%d日 %H:%M")
            elif isinstance(d['create_time'], datetime):
                t = d['create_time'].strftime("%Y年%m月%d日 %H:%M")
            else:
                t = d['create_time']
            rec = d
            rec['create_time'] = t
            result.append(rec)
        return result

    def _encrypt_r(self):
        if self.platform == constants.PLATFORM_ANDROID:
            platform = 'aos'
        elif self.platform == constants.PLATFORM_IOS:
            platform = 'ios'
        else:
            # 手机平台未知？
            err_log = self.config['log']['error']
            utils.loggers.use('error', err_log).info(self.request.headers)
            platform = 'ios'

        key = self.config['ymsecret'][platform]
        appid = self.config['ymappid'][platform]
        aes = AESCipher(key)
        #s = '%s&%s' % (base64.b64encode(self.current_user['oid']),
        s = '%s&%s' % (base64.b64encode(self.session.get('ifa','')),
                       base64.b64encode(str(self.current_user['uid'])))
        r = urllib.quote_plus(appid + aes.encrypt(s))
        # url_earn = urllib.quote('http://w.ymapp.com/wx/%s/lists.html?r=%s&mt=1&bk=1' % (platform, r))
        # url_earn = 'http://w.qiandeer.com/wx/%s/lists.html?r=%s' % (platform, r)
        # url_earn = 'http://au.youmi.net/wx/%s/lists.html?r=%s' % (platform, r)
        url_earn = 'http://w.qiandeer.com/qd/%s/lists.html?r=%s' % ('task', r)
        # url_earn = urllib.quote('http://au.youmi.net/wx/%s/lists.html?r=%s&mt=1&bk=1' % (platform, r))
        return url_earn


class InfoHandler(WebBaseHandler):
    """ 用户资料 """

    @tornado.web.authenticated
    def get(self):
        data = self.current_user

        self.render("setting/info.html", data=data)

    @tornado.web.authenticated
    def post(self):
        params = {
            "uid": self.current_user['uid'],
            "username": self.current_user['username'],
            "sex": self.current_user['sex'],
            "place": self.current_user['place'],
        }
        tasks = self.get_argument('task', "")
        for key in ['username', 'sex', 'work', 'birth']:
            v = self.get_argument(key, '')
            params[key] = tornado.escape.xhtml_escape(v) if v else params[key]
        if int(tasks) == 1:
            result = task.check_task_ios(self.current_user['uid'], 1)
            if result['total'] == 0:
                task.new_task_ios(self.current_user['uid'], 1)
                users.add_tt_points(self.current_user['uid'], 20)
                orders.new_global_order(self.current_user['uid'], self.current_user['points'], 20, 1, u'新手任务：完善资料')
                _today_earn(self, self.current_user['uid'], 20)
                users.update_info(**params)
            else:
                users.update_info(**params)
        else:
            users.update_info(**params)
        self.return_success()

def _today_earn(req, uid, points):
    """ 缓存记录今日赚取 """
    key_name = "qianka:earn:%s:%s" % (uid, date.today().strftime("%Y%m%d"))
    rate = options.get('rate')
    data = req.redis.get(key_name)
    if not data:
        req.redis.setex(key_name, "%.2f" %(float(points)/int(rate)), 86400)
    else:
        req.redis.setex(key_name, "%.2f" %((float(data)+(float(points)/int(rate)))), 86400)


class HeadimgHandler(WebBaseHandler):
    """ 用户头像 """

    @tornado.web.authenticated
    def post(self):
        # 图像压缩 FIXME
        if self.request.files['avatar']:
            avatar = self.request.files['avatar'][0]
            width = 100
            uid_hash = utils.md5(self.current_user['uid'])
            img_dir = 'static/headimg/%s/%s' % (uid_hash[:2], uid_hash[2:4])
            filename = utils.md5(str(time.time()+random.randint(10000, 99999)))
            img_file = '%s/%s.png' % (img_dir, filename)
            # 创建文件夹
            img_path = os.path.join(constants.BASE_DIR, img_dir)
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            f = open(os.path.join(constants.BASE_DIR, img_file), 'wb+')
            f.writelines(avatar['body'])
            f.close()
            im = Image.open(os.path.join(constants.BASE_DIR, img_file))
            ratio = float(width)/im.size[0]
            height = int(im.size[1]*ratio)
            nim = im.resize((width, height), Image.BILINEAR)
            nim.save(os.path.join(constants.BASE_DIR, img_file))
            users.update_avatar(self.current_user['uid'], '/'+img_file)

        self.redirect("/info")


class LogoutHandler(WebBaseHandler):
    """ 注销账号 """

    @tornado.web.authenticated
    def get(self):
        self.redis.delete(self.session.session_id)
        self.redis.delete(self.current_user['oid'])
        self.redirect('/welcome')


class GetIDHandler(WebBaseHandler):
    """ 找回ID """

    @tornado.web.authenticated
    def get(self):
        if self.current_user['phone']:
            pass


class SwitchHandler(WebBaseHandler):
    """ 用户切换账号 """

    @tornado.web.authenticated
    def get(self):
        pass


class PhoneHandler(WebBaseHandler):
    """ 绑定手机号码 """
    @tornado.web.authenticated
    def get(self):
        phone = self.current_user['phone']
        data = {
            'phone': phone if phone else '',
        }
        self.render('setting/phone.html', data=data)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        pkg = str(self.current_user['pkg'])
        flow = str(self.current_user['flow'])
        phone = self.get_argument('phone', '')
        mihe = self.get_argument('type', "")
        count = users.summary_flow()
        if int(count['total']) >= 5500:
            return self.return_error(constants.ERR_PARAMS_NULL)
        user_phone = users.phone_user(phone)
        if int(user_phone['total']) != 0:
            return self.return_error(constants.ERR_INVALID_PHONE)
        code = self.get_argument("code", '')
        if not code or not phone:
            return self.return_error(constants.ERR_PARAMS_NULL)
        elif not phone.isdigit():
            return self.write(constants.ERR_PARAMS_NULL)
        err = captcha.check_sms(phone,  code)
        if not err:
            self.current_user['phone'] = phone
            #流量活动，接口对接
            if pkg == "5" and flow == "1" and mihe != "":
                t = str(int(time.time()))+str(self.current_user['uid'])
                coding = "{\"Activity_id\":\"11\",\"Contract_id\":\"8\",\"Userorid\":\""+t+"\",\"Ordertel\":\""+phone+"\",\"Order_type\":\"1\",\"Userfid\":\"30\",\"Service_code\":\"FS0001\",\"Channel_id\":\"1\",\"Remarks\":\"\",\"Plat_offer_id\":\"30\"}"
                result = self.encrypt_mode_cbc(coding)
                code = self._mcrypt(result)
                data = '{"Partner_no":"100012","Code":\"'+code+'\"}'
                mihe_log = self.config['log']['mihe']
                utils.loggers.use('mihe', mihe_log).info("\r\n"+coding+"\r\n"+code+"\r\n")
                http_client = httpclient.AsyncHTTPClient()
                http_client.fetch("http://218.244.158.167/mihe/Server/Flow.do", callback=self._asy_function, method="POST", body=data)
                #f = urllib.urlopen("http://218.244.158.167/mihe/Server/Flow.do",data)
                #s = f.read()
                #users.flow_user(self.current_user['uid'], 0)
            else:
                  users.set_phone(self.current_user['uid'], phone)
                  return self.return_success()
        else:
            return self.return_error(err)

    def _mcrypt(self, encry):
        letter = 'abcdefghijklmnopqrstuvwxyz'
        result = ''
        for c in encry:
            value = struct.unpack('b', c)[0]
            result += letter[((value>>4) & 15)]
            result += letter[((value) & 15)]
        return result

    def encrypt_mode_cbc(self, data, key='sdosujrr9cHMUG7V', iv = '1034075819834480'):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
       # unpad = lambda s : s[0:-ord(s[-1])]
        obj = AES.new(key, AES.MODE_CBC, iv)
        inputString = pad(data)
        result = obj.encrypt(inputString)
        #print base64.b64encode(result)
        return result

    def _asy_function(self, s):
        mihe_log = self.config['log']['mihe']
        utils.loggers.use('mihe', mihe_log).info("\n===============\n"+self.current_user['phone']+"\n"+str(s.body)+"\n===============")
        if str(s.body).find('00000') == -1:
            return self.return_error(constants.ERR_INTERNAL_ERROR)
        else:
            users.set_phone(self.current_user['uid'], self.current_user['phone'])
            users.flow_user(self.current_user['uid'], 0)
            users.set_flow(self.current_user['uid'],self.current_user['phone'])
            return self.return_success()



# 解绑手机号码
class PhoneUnlockHandler(WebBaseHandler):
    """ 解绑手机号码 """
    @tornado.web.authenticated
    def get(self):
        phone = self.current_user['phone']
        data = {
            'phone': phone if phone else '',
        }
        self.render('setting/switch-phone.html', data=data)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        phone = self.get_argument('phone', '')
        user_phone = users.phone_user(phone)

        if int(user_phone['total']) == 0:
            return self.return_error(constants.ERR_INVALID_PHONE)

        code = self.get_argument("code", '')
        if not code or not phone:
            return self.return_error(constants.ERR_PARAMS_NULL)
        elif not phone.isdigit():
            return self.write(constants.ERR_PARAMS_NULL)
        err = captcha.check_sms(phone,  code)
        if not err:
            self.current_user['phone'] = ''
            users.set_phone(self.current_user['uid'], None)
            return self.return_success()
        else:
            return self.return_error(err)
