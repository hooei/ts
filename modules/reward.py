#!/usb/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author chenjiehua@youmi.net
#

from models import users, orders, options, rule, activity

def task_prorate(user_info, points):
    if user_info['parent']:
        parent = users.get_info(user_info['parent'])
        if parent['platform'] == user_info['platform'] and user_info['platform'] != 0:
            if(parent['vip'] == 1):
                iv_prorate = int(options.get('vip'))
            else:
                iv_prorate = int(rule.get(parent['grade']))
                #iv_prorate = options.get('iv_parent')
            iv_prize = points * iv_prorate / 100
            note = u"您的徒弟 %s 完成任务，你分成 %s%%" % \
                (user_info['tid'], iv_prorate)
            oid = orders.new_global_order(
                parent['uid'], parent['points'], iv_prize,
                orders.OTYPE_INVITE, note)
            users.add_iv_points(parent['uid'], iv_prize)
    if user_info['grandfather']:
        grandfather = users.get_info(user_info['grandfather'])
        if grandfather['platform'] == user_info['platform'] and user_info['platform'] != 0:
            iv_prorate = int(options.get('iv_grandfather'))
            iv_prize = points * iv_prorate / 100
            note = u"您的徒孙 %s 完成任务，你分成 %s%%" % \
                (user_info['tid'], iv_prorate)
            oid = orders.new_global_order(
                grandfather['uid'], grandfather['points'],
                iv_prize, orders.OTYPE_INVITE, note)
            users.add_iv_points(grandfather['uid'], iv_prize)



def task_oneMonth(user_info):
    if user_info['parent']:
        parent = users.get_info(user_info['parent'])
        #iv_prize = options.get('prize')
        info = activity.get('hao')
        iv_prize = int(info['values']) / 100
        #note = u"新生儿摆满月酒！您的徒弟 %s 完成任务，你分成 %s元" % \
        #    (user_info['tid'], iv_prize)
        note = u"恭喜你在土豪行动中成功收徒1名，获得奖励 %s元" % (iv_prize)
        oid = orders.new_global_order(
            parent['uid'], parent['points'], iv_prize*100,
            orders.OTYPE_INVITE, note)
        users.add_iv_points(parent['uid'], iv_prize*100)
