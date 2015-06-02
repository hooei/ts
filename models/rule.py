#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenyongjian@youmi.net
#

import db

@db.db_cache('level_rule')
def get(level):
    data = db.mysql.get(
        "SELECT `value` FROM `level_rule` WHERE `level` = %s", level)
    return data['value'] if data else 0

def get_all(orderby='ASC'):
    return db.mysql.query("SELECT * FROM `level_rule` ORDER BY ID "+orderby)
