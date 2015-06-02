#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

import db

def get_ifa(idfa):
    data = db.mysql.get(
        "SELECT * FROM `wallad_clicks` WHERE `status` = 0 AND \
        `create_time`>=(Curdate()-7) AND `idfa`=%s LIMIT 1", idfa)
    return data if data else None

def set_user_pkg(uid, pkg):
    return db.mysql.execute(
        "UPDATE `users` SET `pkg` = %s WHERE `uid`= %s", pkg, uid)

def get_by_id(id):
    data = db.mysql.get(
        "SELECT * FROM `wallad_clicks` WHERE `id`=%s", id)
    return data if data else None

def delete_by_id(id):
    return db.mysql.execute(
        "DELETE FROM `wallad_clicks` WHERE `id`=%s", id)

def update(msg, wallad_id):
    return db.mysql.execute(
           "UPDATE `wallad_clicks` set `status`=1,`msg`=%s \
           WHERE `id`=%s", msg, wallad_id)
