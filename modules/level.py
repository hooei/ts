#!/usb/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author chenyongjian@youmi.net
#

from models import rule, users
def get_level(uid):
    user_info = users.get_info(uid)
    sons = int(user_info['sons'])
    tt_points = int(user_info['tt_points'])

    level_rule = rule.get_all("DESC")
    for l in level_rule:
        if tt_points >= l['points'] and sons >= l['sons']:
            users.set_user_level(uid,l['level'])
            break

