#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""广告任务回调

"""

import utils
import sys
import ujson as json
import time
import urllib, urllib2
from Crypto.Cipher import AES
from datetime import date
from modules import reward
from models import users, orders, options,activity,rule, wallad_clicks
from protocols import WebBaseHandler

reload(sys)
sys.setdefaultencoding('utf-8')


class CallbackHandler(WebBaseHandler):
    """ 广告回调响应 """

    def get(self, platform):
        # 日志打印
        log_path = self.config['log']['callback']
        self.log_path = log_path
        utils.loggers.use('callback', log_path).info(self.request.uri)
        sign = None
        params = {}
        # save_order 固定用的参数, 但record_time怎么没有被用到。FIXME
        keys = ['order', 'ad', 'adid', 'user', 'points', \
                'price', 'record_time', 'device', 'trade_type']
        if platform == 'youmiios':
            self._platform = 1
            self._platform_name = '有米'
            # 由于有米的联盟任务和其他任务都采用同一个回调接口，需要根据app_id区别
            self._youmi_app_id = self.get_argument('app','')
            params['sign'] = self.get_argument('sign','')
            sign = self.check_sign_ios()
        elif platform == 'wanpuios':
            self._platform = 2
            self._platform_name = '万普'
            params['sign'] = self.get_argument('wapskey','').lower()
            sign = self.check_sign_waps()
        elif platform == 'duomengios':
            self._platform = 3
            self._platform_name = '多盟'
            params['sign'] = self.get_argument('sign','')
            sign = self.check_sign_duomeng()
        elif platform == 'miheios':
            return self.write('mihe')
        elif platform == "zhimengios":
            self._platform = 5
            return self.write("zhimeng")
        else:
            return self.write('what the fuck?')

        # 不同渠道的回调参数不一致，映射参数使之符合callback_orders表
        if platform == 'youmiios':
            for key in keys:
                params[key] = self.get_argument(key, '')
        elif platform == 'wanpuios':
            wanpu_keys = ['order_id', 'ad_name', 'adv_id', 'key','points', \
                    'bill','activate_time','udid','trade_type']
            for i in range(0,len(wanpu_keys)):
                params[keys[i]] = self.get_argument(wanpu_keys[i], '')
        elif platform == 'duomengios':
            duomeng_keys = ['orderid', 'ad', 'adid','user', 'point', \
                    'price', 'ts', 'device','trade_type']
            for i in range(0,len(duomeng_keys)):
                params[keys[i]] = self.get_argument(duomeng_keys[i], '')


        utils.loggers.use('callback', log_path).info('input parmas:'+`params`)
        if sign != params['sign']:
            return self.write('{"message":"无效数据","success":"false"}')
        if not params:
            return self.write('{"message":"无效数据","success":"false"}')

        self.save_order(**params)

        return self.write('{"message":"成功接收","success":"true"}')

    #def post(self):
    #    data = self.arguments()


    def save_order(self, order, ad, adid, user, points,
                   price, record_time, device, sign, trade_type):
        """保存订单"""
        # user_device = users.get_device(user)

        #  mac 有时是BC:XX 有时是BC-XX
        ifa = device.replace('-','').replace(':','').lower()
        # 判断是否一个tid 多个 idfa
        if self._platform == 1 and self._youmi_app_id == self.config['ymappid']['ios']:
            pass
        else:
            tid = users.get_ifa_tid(ifa)
            count = users.get_count_ifa(tid)
            if int(count) > 1:
                log_path = self.config['log']['order']
                utils.loggers.use('order', log_path).info("\n"+str(tid)+":"+str(count)+"\n"+"ifa:"+str(ifa)+"\n")
                return self.write("invid user")

        user_device = users.get_device_byifa(ifa)
        if not user_device:
            user_device = users.get_device_bymac(device)
            if not user_device:
                user_device = users.get_device_byifa(user)
                if not user_device:
                    user_device = users.get_device(user)
                    if not user_device:
                        utils.loggers.use('callback', self.log_path).info('not user')
                        return self.write('not user')
        user_info = users.get_info(user_device.get('uid', 0))
        if not user_info:
            utils.loggers.use('callback', self.log_path).info('not user')
            return self.write('not user')
        # 小助手不加积分
        try:
            if int(adid) == 7658:
                return self.write('qiankaxiaozhushou')
        except:
            pass
        order_info = orders.get_callback_order(order)
        if order_info:
            utils.loggers.use('callback', self.log_path).info('had points')
            return self.write('had points')
        # 用户被邀请
        if user_info['parent']:
            # 师傅收益缓存今日赚取
            parent = users.get_info(int(user_info['parent']))
            # 解决 Android 和 iOS 在同一个数据库造成的师徒不在同一平台的问题
            if parent['platform'] == user_info['platform'] and user_info['platform'] != 0:
                reward.task_prorate(user_info, int(points))
                if(parent['vip'] == 1):
                    iv_prorate = options.get('vip')
                else:
                    iv_prorate = rule.get(parent['grade'])
                    #iv_prorate = options.get('iv_parent')
                self._today_earn(user_info['parent'],"%.2f" %(int(points) * int(iv_prorate)/100))
                #人人VIP活动
                self._vip_task(user_info)

        if user_info['grandfather']:
            grandfather = users.get_info(int(user_info['grandfather']))
            if grandfather['platform'] == user_info['platform']:
                iv_gprorate = options.get('iv_grandfather')
                self._today_earn(user_info['grandfather'], "%.2f" %(int(points) * int(iv_gprorate)/100))
        count_otype = int(orders.count_callback_orders(user_info['uid'])['dcount'])
        # 土豪行动奖励
        # 设定开始结束时间
        day = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        data = activity.get('hao')
        #添加活动状态控制
        if data['status'] != 0:
            if user_info['parent'] and count_otype == 0 and parent['platform'] == user_info['platform'] and user_info['platform'] != 0:
                parent = users.get_info(int(user_info['parent']))
                iv_prize = int(data['values'])
                if parent['vip'] == 1:
                    reward.task_oneMonth(user_info)
                    self._today_earn(user_info['parent'],"%.2f" %(iv_prize))
                elif day >= str(data['start_time']) and day < str(data['end_time']):
                    reward.task_oneMonth(user_info)
                    self._today_earn(user_info['parent'],"%.2f" %(iv_prize))

        if not order_info:
            if trade_type == '':
                trade_type = 1
            # 非联盟任务
            if self._platform == 1 and self._youmi_app_id == self.config['ymappid']['ios']:
                if int(trade_type) == 1:
                    note = u"成功下载安装「%s」" % ad
                elif int(trade_type) == 2:
                    note = u"成功完成深度任务「%s」" % ad
            # 联盟任务
            else:
                if int(trade_type) == 1:
                    note = u"成功完成%s联盟任务「%s」" % (self._platform_name,ad)
                elif int(trade_type) == 2:
                    note = u"成功完成%s联盟深度任务「%s」" % (self._platform_name,ad)

            oid = orders.new_global_order(
                user_info['uid'], user_info['points'], points,
                orders.OTYPE_TASK, note)
            users.add_tt_points(user_info['uid'], points)
            params = { "order": order, "oid": oid, "ad": ad, "adid": adid, "uid": user_info['uid'], "points": points,
                "price": price,
                "device": device,
                "sig": sign,
                "platform": 2,
                "trade_type": trade_type,
                "ad_source": self._platform,
                "pkg" : user_info['pkg']
            }
            orders.new_callback_order(**params)

            utils.loggers.use('callback', self.log_path).info('save_order:'+`params`)
            # self._youmi_ad(ifa)
            self._today_earn(user_info['uid'], points)
            self._callback_record(user_info['uid'], ad, adid, points, trade_type)

    def _vip_task(self, user_info):
        #人人都是VIP
        act = activity.get('vip')
        if act['status'] == 1:
            day = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            if day >= str(act['start_time']) and day <str(act['end_time']):
                count = orders.count_callback_order(user_info['uid'])
                if count['total'] == 0:
                    activity.add_vip_task(user_info['parent'], user_info['uid'])
                    total = activity.count_vip_task(user_info['parent'])
                    if total['total'] < 9:
                        money = 2
                    elif total['total']>=10 and total['total']<50:
                        money = 2.5
                    elif total['total'] >= 50:
                        money = 3
                    orders.new_global_order(
                    user_info['parent'], user_info['points'], float(money*100),
                    2, u"恭喜你在粉丝节成功收得一名徒弟，奖励%s元。" % (money))
                    self._today_earn(user_info['parent'],"%.2f" % (money*100))
                    users.add_tt_points(user_info['parent'], float(money * 100))

    def _youmi_ad(self, ifa):
        # 有米推广
#        device = str(params['device'])
#        ifa = device.replace('-','').replace(':','').lower()
        user_info = users.get_device_byifa(ifa)

        adinfo = wallad_clicks.get_ifa(ifa)
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
                WHERE `id`=%s", user_info['uid'], msg, adinfo['id'])
            wallad_clicks.set_user_pkg(user_info['uid'], adinfo['adserver'])

    def check_sign_ios(self):
        """ ios验证签名 """
        args = self.request.arguments
        kv = []
        for key in args:
            if key != 'sign':
                value = args[key][0].decode('utf-8')
                kv.append('%s=%s' % (key, value))
        raw_str = ''
        for s in sorted(kv):
            raw_str += s
        if self._youmi_app_id == self.config['ymappid']['ios']:
            raw_str += self.config['ymserver_key']['ios']
        else:
            raw_str += self.config['youmi_union_key']['ios']
        return utils.md5(raw_str)

    def check_sign_waps(self):
        """ 万普验证签名 """
        args = self.request.arguments
        kv = ''
        adv_id =  args['adv_id'][0]
        app_id =  args['app_id'][0]
        key =  args['key'][0]
        udid =  args['udid'][0]
        bill  =  args['bill'][0]
        points =  args['points'][0]
        order_id =  args['order_id'][0]

        time = args['activate_time'][0]
        ac_time = {'activate_time':time}
        encode_time = urllib.urlencode(ac_time)[14:]

        kv = adv_id + app_id + key + udid + bill + points + encode_time + order_id + self.config['wanpu_key']['ios']

        utils.loggers.use('callback', self.log_path).info('[wanpu_before_md5]'+kv)
        utils.loggers.use('callback', self.log_path).info('[wanpu_md5]'+utils.md5(kv))
        return utils.md5(kv)

    def check_sign_duomeng(self):
        """ duomeng验证签名 """
        args = self.request.arguments
        kv = []
        for key in args:
            if key != 'sign':
                value = args[key][0].decode('utf-8')
                kv.append('%s=%s' % (key, value))
        raw_str = ''
        for s in sorted(kv):
            raw_str += s
        raw_str += self.config['duomeng_key']['ios']

        utils.loggers.use('callback', self.log_path).info('[duomeng_before_md5]'+raw_str)
        utils.loggers.use('callback', self.log_path).info('[duomeng_md5]'+utils.md5(raw_str))
        return utils.md5(raw_str)
    def _today_earn(self, uid, points):
        """ 缓存记录今日赚取 """
        key_name = "qianka:earn:%s:%s" % (uid, date.today().strftime("%Y%m%d"))
        rate = options.get('rate')
        data = self.redis.get(key_name)
        if not data:
            self.redis.setex(key_name, "%.2f" %(float(points)/int(rate)), 86400)
        else:
            self.redis.setex(key_name, "%.2f" %((float(data)+(float(points)/int(rate)))), 86400)

    def _callback_record(self, uid, ad, adid, points, trade_type):
        rate = options.get('rate')
        """ 缓存回调记录，用于客户端轮询 """
        rec = {
            "ad": ad,
            "watid": adid,
            "points": "%.2f" %(float(points)/int(rate)),
            "aname": self.config['app']['name'],
            "trade_type": trade_type,
            "msg": "恭喜你, 完成%s联盟的任务「%s」"  % (self._platform_name, ad),
        }
        if self._platform == 1 and self._youmi_app_id == self.config['ymappid']['ios']:
            rec['msg']='恭喜你，完成任务「%s」' % ad
        key_name = "qianka:callback:%s" % uid
        data = self.redis.get(key_name)
        if not data:
            result = []
            result.append(rec)
        else:
            result = json.loads(data)
            result.append(rec)
        self.redis.setex(key_name, json.dumps(result), 86400*7)

class MiheCallbackHandler(WebBaseHandler):
    """ 米禾回调响应 """

    def post(self):
        body = self.request.body
        if not body:
            return self.write("-1 no post")
        j = json.loads(body)
        if not j:
            return self.write("-1 not currect")
        partner_no = str(j['Partner_no'])
        code = str(j['Code'])
        bytes = self._decodeBytes(code)
        data = self.decrypt_mode_cbc(bytes)
        log_path = self.config['log']['callback']
        utils.loggers.use('callback', log_path).info("\n partner_no:"+partner_no+"code:"+str(data))
        data = data.decode('gbk')
        data = json.loads(data)
        user_info = users.get_byphone(str(data['Ordertel']))
        if not user_info:
            utils.loggers.use('callback', log_path).info("\n no user = "+data['Ordertel'])
            return self.write("1")
        utils.loggers.use('callback', log_path).info("\n code:"+data['Result_code']+data['Remarks']+data['Ordertel'])
        return self.write("1")


    def _decodeBytes(self, string):
        letter = 'abcdefghijklmnopqrstuvwxyz'
        byte = ''
        i = 0
        while i<len(string):
            c = string[i]
            char_value = letter.find(c)<<4
            c = string[i+1]
            char_value += letter.find(c)
            byte+=chr(char_value)
            i+=2
        return byte

    def decrypt_mode_cbc(self, encrypted, key='sdosujrr9cHMUG7V', iv = '1034075819834480'):
        unpad = lambda s : s[0:-ord(s[-1])]
        if encrypted is not '':
            obj = AES.new(key, AES.MODE_CBC, iv)
            return unpad(obj.decrypt(encrypted))
        else:
            return False
