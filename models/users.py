#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

"""用户相关操作

"""

import db
import time

""" users表 """
def new_user(ip, ip_address, pkg):
    number = int(time.time()) - 1422000000
    user=db.mysql.execute(
        "INSERT INTO `users`(`ip`, `ip_address`, `pkg`)"
        "VALUES(%s, %s, %s)", ip, ip_address, pkg)
    db.mysql.execute(
        "UPDATE `users` SET `tid` = %s WHERE `uid` = %s", \
        int(number)+int(user), user)
    return user

#米禾推广
def flow_user(uid, flow):
    return db.mysql.execute(
        "UPDATE `users` SET `flow` = %s WHERE `uid` = %s", flow, uid
    )

def summary_flow():
	 return db.mysql.get(
        "SELECT COUNT(*) AS total FROM `flow`"
    )
def set_flow(uid, phone):
	return db.mysql.execute(
		"INSERT INTO `flow`(`uid`, `phone`)"
        "VALUES(%s, %s)", uid, phone)

#手机检测
def phone_user(phone):
    return db.mysql.get(
        "SELECT COUNT(*) AS total FROM `users` WHERE `phone` = %s AND `platform` = 2", phone
    )

def get_byphone(phone):
	return db.mysql.get(
		"SELECT * FROM `users` WHERE `phone` = %s", phone
	)

def get_count_byip(ip):
    return db.mysql.get(
            "SELECT count(*) AS total FROM `users` WHERE `ip` = %s", ip
        )

def get_info(uid):
    return db.mysql.get(
        "SELECT * FROM `users` WHERE `uid` = %s", uid)

def get_info_bytid(tid):
    return db.mysql.get(
        "SELECT * FROM `users` WHERE `tid` = %s", tid)

def set_user_bonus(uid):
    return db.mysql.execute(
        "UPDATE `users` SET `gift` = 0  WHERE `uid` = %s", uid)

@db.db_cache('user_total', count=0, ttl=300)
def count_users():
    data = db.mysql.get(
        "SELECT count(`uid`) AS dcount, sum(`sons`) AS dsum FROM `users`")
    return data

def add_tt_points(uid, points):
    return db.mysql.execute(
        "UPDATE `users` SET `points` = `points` + %s, "
        "`tt_points` = `tt_points` + %s WHERE `uid` = %s",
        points, points, uid)

def add_iv_points(uid, points):
    return db.mysql.execute(
        "UPDATE `users` SET `points` = `points` + %s, "
        "`iv_points` = `iv_points` + %s, `tt_points` = `tt_points` + %s "
        "WHERE `uid` = %s", points, points, points, uid)

def sub_ex_points(uid, points):
    return db.mysql.execute(
        "UPDATE `users` SET `points` = `points` - %s, "
        "`ex_points` = `ex_points` + %s WHERE `uid` = %s",
        points, points, uid)

def add_ex_points(uid, points):
    return db.mysql.execute(
        "UPDATE `users` SET `points` = `points` + %s, "
        "`ex_points` = `ex_points` - %s WHERE `uid` = %s",
        points, points, uid)

def set_invite(uid, parent, grandfather):
    return db.mysql.execute(
        "UPDATE `users` SET `parent` = %s, `grandfather` = %s "
        "WHERE `uid` = %s", parent, grandfather, uid)

def add_invite(uid, son=0, grandson=0):
    return db.mysql.execute(
        "UPDATE `users` SET `sons` = `sons` + %s, "
        "`grandsons` = `grandsons` + %s WHERE `uid` = %s ",
        son, grandson, uid)

def update_info(uid, username, sex, place, birth, work):
    return db.mysql.execute(
        "UPDATE `users` SET `username` = %s, `sex` = %s, `place` = %s, `birth` = %s, `work` = %s "
        "WHERE `uid` = %s", username, sex, place, birth, work, uid)

def update_avatar(uid, avatar):
    return db.mysql.execute(
        "UPDATE `users` SET `headimg` = %s WHERE `uid` = %s",
        avatar, uid)

def set_platform(uid, platform):
    return db.mysql.execute(
        "UPDATE `users` SET `platform` = %s WHERE `uid` = %s",
        platform, uid)

def set_phone(uid, phone):
    return db.mysql.execute(
        "UPDATE `users` SET `phone` = %s, `flow` = 0 WHERE `uid` = %s",
        phone, uid)

def set_last_login(uid, time):
    return db.mysql.execute(
        "UPDATE `users` SET `last_login` = %s WHERE `uid` = %s",
        time, uid)
"""用户等级"""
def set_user_level(uid,level):
    return db.mysql.execute(
        "UPDATE `users` SET `grade` = %s WHERE `uid` = %s",level,uid
    )

""" devices表 """
def new_device(oid, uid, cid, mac, ifa, aicid, udid, attr, tid, un):
    return db.mysql.execute(
        "INSERT INTO `devices`(`oid`, `uid`, `cid`, `mac`, `ifa`, "
        "`aicid`, `udid`, `attr`, `tid`, `device_name`)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        oid, uid, cid, mac, ifa, aicid, udid, attr, tid, un)

@db.db_cache("device")
def get_device(oid):
    return db.mysql.get(
        "SELECT * FROM `devices` WHERE `oid` = %s LIMIT 1", oid)

@db.db_cache("device_ifa")
def get_device_byifa(ifa):
    return db.mysql.get(
        "SELECT * FROM `devices` WHERE `ifa` = %s LIMIT 1", ifa)

@db.db_cache("device_mac")
def get_device_bymac(mac):
    return db.mysql.get(
        "SELECT * FROM `devices` WHERE `mac` = %s LIMIT 1", mac)

def get_device_byuid(uid):
	return db.mysql.query(
		 "SELECT * FROM `devices` WHERE `uid` = %s", uid
	)

def update_oid(ifa, noid, ooid):
    return db.mysql.execute(
        "UPDATE `devices` SET `same_oid`=%s, `oid` = %s, \
        `old_oid` = %s WHERE `ifa` = %s",
        1,noid, ooid, ifa)

def update_dname(ifa, name):
    return db.mysql.execute(
        "UPDATE `devices` SET `device_name`=%s WHERE `ifa` = %s" ,name, ifa)

def get_user_ip(uid, ip):
    return db.mysql.get(
        "SELECT * FROM `ip_info` WHERE `uid` = %s  AND `ip` = %s LIMIT 1", uid, ip)

def set_user_ip(ip, uid, ip_address):
    ip_info=db.mysql.execute(
        "INSERT INTO `ip_info`(`ip`, `uid`, `ip_address`)"
        "VALUES(%s, %s, %s)", ip, uid, ip_address)
    return ip_info

def get_ifa_tid(ifa):
    data = db.mysql.get(
        "SELECT `tid` FROM `devices` WHERE `ifa` = %s", ifa
    )
    return data['tid']

def get_count_ifa(tid):
    data = db.mysql.get(
        "SELECT COUNT(*) AS total FROM `devices` WHERE `tid` = %s", tid
    )
    return data['total']

def set_bonus(uid, bonus):
    ''''记录用户注册时收获红包bonus的大小'''
    print "UPDATE `users` SET `bonus` =  %s where  uid  = %s"  % ( bonus, uid)
    return db.mysql.execute("UPDATE `users` SET `bonus` =  %s where  uid  = %s" , bonus, uid)

