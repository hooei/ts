#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""客户端请求相关

"""

import IP
import ujson as json
import time
import urllib, urllib2
import tornado.web
import constants
import utils
from models import options, orders, wallad_clicks
from datetime import date
from tornado import httpclient
from protocols import JSONBaseHandler
from models import users, invites

class LoginHandler(JSONBaseHandler):
    """ 用户登陆

    客户端回调服务器，绑定oid跟ssid, 实现用户登陆
    首次请求，自动帮用户注册账号
    """

    @tornado.web.asynchronous
    def post(self):
        s = self.request.body
        print `s` + 's--------------------------'
        params = self.decrypt_params(s)
        print `params` + 'params'
        if not params.get('ifa', None):
            return self.return_error(constants.ERR_PARAMS_NULL)

        # 判断用户是否存在，不存在则新建
        if users.get_device_byifa(params['ifa']):
            #uid=users.get_device(params['oid'])['uid']
            userinfo=users.get_device_byifa(params['ifa'])
            uid = userinfo['uid']
            user_log = self.config['log']['user']
            utils.loggers.use('user', user_log).info('userinfo='+`userinfo`+'&params='+`params`)
            self._set_ssid(params['ssid'], params['ifa'], params['oid'], params['av'])
            # print `userinfo['oid']` + 'user oid
            #if (userinfo['oid'] != params['oid']):
            #    if userinfo['oid']!= utils.md5(params['ifa']):
            if userinfo['oid']!= params['ifa']:
                    # users.update_oid(params['ifa'], params['oid'], userinfo['oid'])
                users.update_oid(params['ifa'], params['ifa'], userinfo['oid'])
                self._set_ssid(params['ssid'], params['ifa'], params['ifa'], params['av'])
                ifa = "qianka:device_ifa:" + params['ifa']
                self.redis.delete(ifa)
                #self.redis.setex(params['ifa'])
            else:
                self._set_ssid(params['ssid'], params['ifa'], params['ifa'], params['av'])
            tid = users.get_info(uid)['tid']
            self.return_result({"userid": tid})
            #return self.return_success()
        else:
            self._bind_device(params)

    def _set_ssid(self, ssid, ifa, oid, av, first=0):
        self.redis.delete(self.redis.get(oid))
        self.redis.setex(ssid,
                         json.dumps({"oid": oid, "ifa": ifa, "av": av, "first": first}),
                         86400)
        self.redis.setex(oid, ssid, 86400)

    def _bind_device(self, params={}):
        """ 请求中间层绑定设备 """
        # self.request.remote_ip()
        deviceinfo = users.get_device(params['oid'])
        # print `params['oid']` +  'params oid'
        # print 'deviceinfo' + `deviceinfo`

        # 如果有重复oid
        if deviceinfo:
            noid = utils.md5(params['ifa'])
            deviceinfo2 = users.get_device(noid)
            if deviceinfo2:
                utils.loggers.use('device', self.config['log']['device']).info(`noid`+'md5Ifa')
                self.return_error(constants.ERR_MD5IFA_FAIL)
        else:
            noid = params['oid']
        ip = self.request.remote_ip
        keys = ['cid', 'appid', 'opid', 'mac', 'udid', 'ifa', 'aicid', \
                'batsn', 'fcsn', 'bcsn', 'tid', 'av', 'sv', 'attr', \
                'rsd', 'un', 'oid', 'ssid', 'scode', 's', 'cne', 'ex']
        req_params = {}
        for key in keys:
            req_params[key] = params.get(key, '')
        print `req_params` + '-------------------------'
        req_params['pd'] = 3
        req_params['ip'] = ip
        if not params.get('s', ''):
            params['s']=''
            req_params['s']=''
        else:
            req_params['s'] = params['s']
        req_params['rsd'] = utils.md5(str(time.time()))[10:20]
        # iOS & Android 的绑定区分 FIXME
        req_params['appid'] = self.config['ymappid']['ios']
        # req_params['opid'] = params['oid']
        # req_params['opid'] = noid
        req_params['opid'] = params['ifa']
        raw_str = ''.join(["%s=%s" % (key, req_params[key]) \
                           for key in sorted(req_params.keys())])
        raw_str += self.config['ymsecret']['ios']
        req_params['sign'] = utils.md5(raw_str)
        base_url = "http://stat.gw.youmi.net/ios/v3/qd_dv_vld"
        url = "%s?%s" % (base_url, urllib.urlencode(req_params))
        utils.loggers.use('device', self.config['log']['device']).info(`url`+'&ip='+`ip`)
        # FIXME WSGI无法使用异步非阻塞式请求
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(url, self._handle_callback)
        self._user_params = {
            "scode": params.get('scode', ''),
            "ssid": params.get('ssid', ''),
            #"oid": noid,
            #"oid": params['oid'],
            # 绑定ifa替换oid
            "oid": params.get('ifa', ''),
            "cid": params.get('cid', ''),
            "mac": params.get('mac', ''),
            "ifa": params.get('ifa', ''),
            "aicid": params.get('aicid', ''),
            "udid": params.get('udid', ''),
            "attr": params.get('attr', ''),
            "av": params.get('av', ''),
            "tid": params.get('tid', ''),
            "un": utils.md5(req_params['un']),
            "cne": params.get('cne', ''),
            #"ex" : params.get('ex', '')
        }

    def _handle_callback(self, response):
        utils.loggers.use('device', self.config['log']['device']).info(response)
        utils.loggers.use('device', self.config['log']['device']).info(response.body)
        if response.code != 200:
            return self.return_error(constants.ERR_BIND_FAIL)
        result = json.loads(response.body)
        #print `result` + 'result----------------------------'
        if result['c'] != 0:
            utils.loggers.use('device', self.config['log']['device']).info(`self._user_params`+'&result='+`result`)
            return self.return_error_bind(result['c'])
        else:
            # self.return_success()
            av = self._user_params.pop('av')
            self._set_ssid(self._user_params.pop('ssid'), self._user_params['ifa'], self._user_params['ifa'], av, first=1)
            uid = self._new_user()
            # 有米推广
            """adinfo = wallad_clicks.get_ifa(self._user_params['ifa'])
            if adinfo:
                callback_url = adinfo['callback_url']
                try:
                    msg = str(urllib2.urlopen(callback_url).read())
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                except urllib2.URLError,e:
                    msg = str(e)
                self.db.execute(
                    "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s \
                    WHERE `id`=%s", uid, msg, adinfo['id'])
                wallad_clicks.set_user_pkg(uid, adinfo['adserver'])"""
            tid = users.get_info(uid)['tid']
            self.return_result({
                "userid": tid })
        # self.finish()

    def _new_user(self):
        # ip = str(self.request.headers.get('X-Real-Ip', '')).split(',')[0]
        scode = self._user_params.pop('scode' ,'')
        cne = self._user_params.pop('cne')
        pkg = cne
        if scode == 'qianlu_pkg1':
            pkg = 1
        if pkg == '':
            pkg = 0
        user_params = {
            "ip": self.request.remote_ip,
            "ip_address": IP.find(self.request.remote_ip),
            "pkg": pkg,
        }
        # 渠道点击统计,先写入redis，再通过脚本将redis中的数据同步到数据库，每小时执行一次
        value = self.redis.get("qianka:channel_click:"+cne)
        if not value:
            value = 0
            self.redis.set("qianka:channel_click:"+cne,1)
        else:
            value = int(value)+1
            self.redis.set("qianka:channel_click:"+cne,value)
        utils.loggers.use('channel_click', self.config['log']['channel_click']).info("channel:"+`cne`+" "+`value`)
        uid = users.new_user(**user_params)
        if int(pkg) == 5:
            users.flow_user(uid, 1)
        self._user_params['uid'] = uid


        users.new_device(**self._user_params)
        # 是否邀请，考虑使用队列来减少接口处理时间 FIXME
        if scode and (scode!='qianlu_pkg1'):
            self._set_invite(uid, scode)
            key_name = "qianka:scode:%s" % uid
            self.redis.setex(key_name, scode, 600)
        return uid

    def _set_invite(self, uid, code):
        """ 邀请判断处理 """
        parent_uid = utils.base34.decode(str(code).upper())
        parent = users.get_info(parent_uid)
        if not parent:
            return
        user = users.get_info(uid)
        if str(parent['platform']) != "2":
            utils.loggers.use('user', self.config['log']['user']).info('[invite] different platform ! parent:'+str(parent_uid)+' child:'+str(uid))
            return
        rate = int(options.get('rate'))
        users.add_tt_points(uid, 3*rate)
        orders.new_global_order(uid, 0, \
            3*rate, 4, u'新手红包')
        # 一级邀请
        users.set_invite(uid, parent['uid'], parent['parent'])
        ad_kidd=u'恭喜您成功收获了一名徒弟'
        orders.new_global_order(parent['uid'], parent['points'], 0, 2, ad_kidd)
        self._add_invite(parent['uid'], son=1)
        # 判断是否存在二级邀请
        if parent['parent']:
            ad_son=u'恭喜您成功收获了一名徒孙!'
            grandfather = users.get_info(parent['parent'])
            orders.new_global_order(parent['parent'], grandfather['points'], 0, 2, ad_son)
            self._add_invite(parent['parent'], grandson=1)

    def _add_invite(self, uid, son=0, grandson=0):
        """ 增加邀请人数、记录 """
        users.add_invite(uid, son, grandson)
        today = date.today().strftime("%Y%m%d")
        if invites.get_invite(uid, today):
            invites.add_invite(uid, son, grandson)
        else:
            invites.new_invite(uid, son, grandson)


    @tornado.web.asynchronous
    def get(self):
        """ 测试 """
        params = {}
        for key in self.request.arguments.keys():
            params[key] = self.get_argument(key, '')

        if not params.get('oid', ''):
            return self.return_error(constants.ERR_PARAMS_NULL)

        # 判断用户是否存在，不存在则新建
        if users.get_device_byifa(params['ifa']):
            self._set_ssid(params['ssid'], params['oid'])
            return self.return_success()
        else:
            self._bind_device(params)


class GetMsgHandler(JSONBaseHandler):
    """积分轮询

    客户端轮询服务器，请求用户积分是否到账，用于消息推送
    """

    def get(self):
        #oid = self.get_argument('oid')
        #params = {"oid": oid}
        s = self.get_argument('s')
        params = self.decrypt_params(s)
        if not params.get('ifa', None):
            return self.return_error(constants.ERR_PARAMS_NULL)
        #if not params.get('oid', None):
        #    return self.return_error(constants.ERR_PARAMS_NULL)
        # FIXME 小助手新版换ifa
        device = users.get_device_byifa(params['ifa'])
        # device = users.get_device(params['oid'])
        if device:
            key_name = "qianka:callback:%s" % device['uid']
            raw_data = self.redis.get(key_name)
            if raw_data:
                result = json.loads(raw_data)
                # 测试完成后取消注释 FIXME
                self.redis.delete(key_name)
                # print result
            else:
                result = []
        else:
            result = []
        self.return_result(result)
