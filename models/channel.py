#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: luojianqiang@youmi.net
#

import db


def get_by_id(id):
    data = db.mysql.get(
        "SELECT * FROM `channel` WHERE `id` = %s ", id)
    return data if data else 0


