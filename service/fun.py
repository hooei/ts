#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

""" 娱乐信息相关

"""
import tornado.web
import random
import time
import constants
from datetime import date
from protocols import WebBaseHandler
from models import activity,users, orders, options

class LotteryHandler(WebBaseHandler):
    """ 抽奖页面 """
    @tornado.web.authenticated
    def get(self):
        dating = date.today()
        dating = dating.strftime('%Y-%m-%d')
        count = activity.check_prize(self.current_user['uid'], dating)
        if count['total'] == 0:
            time = 1
        else:
            time = 0
        self.render('fun/lottery.html', time=time)

    @tornado.web.authenticated
    def post(self):
        act = activity.get('fun')
        if act['status'] == 1:
            day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if day > str(act['start_time']) and day < str(act['end_time']):
                dating = date.today()
                dating = dating.strftime('%Y-%m-%d')
                count = activity.check_prize(self.current_user['uid'], dating)
                if count['total'] == 0:
                    prize_list = activity.get_prize()
                    result = self._get_rand(prize_list, dating)
                    money = int(result['money'] * 100)
                    users.add_tt_points(self.current_user['uid'], money)
                    orders.new_global_order(self.current_user['uid'], self.current_user['points'], money, 4, u'每日抽奖')
                    self._today_earn(self.current_user['uid'], money)
                    return self.return_result({
                        'index':result['place'],
                        'name' :result['prize'],
                        'money':result['money']
                        })
                else:
                    return self.return_error(constants.ERR_INVALID_TIME)
            else:
                return self.return_error(constants.ERR_INVALID_DATE)
        else:
            return self.return_error(constants.ERR_INVALID_DATE)


    def _get_rand(self, prize_list, dating):
        summary = 0
        result = {}
        for i in range(len(prize_list)):
            if prize_list[i]['count'] == 0:
                prize_list[i]['percent'] = 0
            summary += prize_list[i]['percent']

        for i in range(len(prize_list)):
            randNum = random.randint(1, summary)
            if randNum <= int(prize_list[i]['percent']):
                result = prize_list[i]
                break
            else:
                summary -= int(prize_list[i]['percent'])

        if result['id'] == 6:
            r = random.uniform(0.04, 0.1)
            r = round(r, 2)
            gift = [
                {'money': 1, 'percent':1},
                {'money': 0.2, 'percent':2},
                {'money': r, 'percent':97},
            ]
            count = 100
            for i in range(len(gift)):
                randNum = random.randint(1, count)
                if randNum <= int(gift[i]['percent']):
                    money = gift[i]['money']
                    break
                else:
                    count -= int(gift[i]['percent'])
            result.update({'money':money})
            activity.add_prize(self.current_user['uid'],result['id'],result['money'],dating)
            return result
        else:
            result.update({'money':0})
            activity.add_prize(self.current_user['uid'],result['id'],result['money'],dating)
            return result

    def _today_earn(self, uid, points):
        key_name = "qianka:earn:%s:%s" % (uid, date.today().strftime("%Y%m%d"))
        rate = options.get('rate')
        data = self.redis.get(key_name)
        if not data:
            self.redis.setex(key_name, "%.2f" %(float(points)/int(rate)), 86400)
        else:
            self.redis.setex(key_name, "%.2f" %((float(data)+(float(points)/int(rate)))), 86400)
