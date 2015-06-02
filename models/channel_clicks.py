#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: luojianqiang@youmi.net
#

import db
import time

def get_by_id(cid, day):
    data = db.mysql.get(
        "SELECT * FROM `channel_clicks` WHERE `cid` = %s and `day`= %s", cid, day)
    return data if data else 0

def get_all_channel_ids():
    data = db.mysql.query(
        "SELECT `id` FROM `channel` order by `id`")
    return data if data else []

def init_today(cid):
    today = time.strftime("%Y%m%d")
    data = get_by_id(cid, today)
    if not data:
        db.mysql.execute(
            "insert into `channel_clicks` (cid,day,click) values(%s,%s,0)",cid, today)

def increase_click(cid, count):
    return db.mysql.execute(
        "update `channel_clicks` set `click`=`click`+%s WHERE `cid` = %s and day= %s", count, cid, time.strftime("%Y%m%d"))
