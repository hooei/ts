#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

"""订单相关操作

"""

import db

# 全局订单 类型
OTYPE_TASK = 1
OTYPE_INVITE = 2
OTYPE_EXCHANGE = 3

# 兑换订单 状态
EXSTS_AUDIT = 10
EXSTS_PASS = 11
EXSTS_REJECT = 12
EXSTS_SUCC = 13
EXSTS_FAIL = 14

""" callback_orders """
def new_callback_order(order, oid, ad, adid, uid, points,
                       price, device, sig, platform, trade_type, ad_source, pkg):
    return db.mysql.execute(
        "INSERT INTO `callback_orders`(`order`, `oid`, `ad`, `adid`,"
        "`uid`, `points`, `price`, `device`, `sig`, `platform`, `trade_type`,`ad_source`,`pkg`)"
        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        order, oid, ad, adid, uid, points, price, device, sig, platform, trade_type,ad_source, pkg)

@db.db_cache("callback")
def get_callback_order(order):
    return db.mysql.get(
        "SELECT * FROM `callback_orders` WHERE `order` = %s", order)

def count_callback_order(uid):
	return db.mysql.get(
		"SELECT COUNT(*) AS total FROM `callback_orders` WHERE `uid` = %s", uid
	)

""" global_orders """

def new_global_order(uid, last, points, otype, note):
    db.del_cache("global", uid)
    db.del_cache("global", uid, otype)
    return db.mysql.execute(
        "INSERT INTO `global_orders`(`uid`, `last`, `points`,"
        "`otype`, `note`)VALUES(%s, %s, %s, %s, %s)",
        uid, last, points, otype, note)

@db.db_cache("global")
def get_global_orders(uid):
    return db.mysql.query(
        "SELECT * FROM `global_orders` WHERE `uid` = %s "
        "ORDER BY `id` DESC LIMIT 50", uid)

@db.db_cache("global", 2)
def get_otype_orders(uid, otype):
    return db.mysql.query(
        "SELECT * FROM `global_orders` WHERE `uid` = %s AND "
        "`otype` = %s ORDER BY `id` DESC LIMIT 50", uid, otype)

def count_otype_orders(uid, otype):
	return db.mysql.get(
		"SELECT COUNT(*) AS total FROM `global_orders` WHERE `uid` = %s AND "
        "`otype` = %s", uid, otype)

def count_callback_orders(uid):
    return db.mysql.get(
        "SELECT count(`id`) AS dcount FROM `callback_orders` WHERE `uid` = %s", uid)

# """ exchange_orders """
# def new_exchange_order(uid, oid, points, face_price, actual_price, description,
#                 address, order_num, extype, ip, ip_address, status, wait_audit, pkg, bonus):
#     return db.mysql.execute(
#         "INSERT INTO `exchange_orders`(`uid`, `oid`, `points`, `face_price`, "
#         "`actual_price`, `description`, `address`, `order_num`, `extype`, `ip`, "
#         "`ip_address`, `status`, `wait_audit`, `pkg`)VALUES(%s, %s, %s, %s, %s, %s, %s,"
#         "%s, %s, %s, %s, %s, %s, %s)", uid, oid, points, face_price, actual_price,
#         description, address, order_num, extype, ip, ip_address, status, wait_audit, pkg)

""" exchange_orders """
def new_exchange_order(uid, oid, points, face_price, actual_price, description,
            address, order_num, extype, ip, ip_address, status, wait_audit, pkg, bonus, platform=2):
    return db.mysql.execute(
        "INSERT INTO `exchange_orders`(`uid`, `oid`, `points`, `face_price`, "
        "`actual_price`, `description`, `address`, `order_num`, `extype`, `ip`, "
        "`ip_address`, `status`, `wait_audit`, `platform`, `pkg`, `bonus`)VALUES(%s, %s, %s, %s, %s, %s, %s,"
        "%s, %s, %s, %s, %s, %s, %s, %s, %s)", uid, oid, points, face_price, actual_price,
        description, address, order_num, extype, ip, ip_address, status, wait_audit, platform, pkg, bonus)

def exists_exchange(uid):
    """判断该s用户是否已经有历史兑换记录"""
    return  None != db.mysql.get("SELECT uid  FROM `exchange_orders` WHERE `uid` = %s limit 1", uid) 


def set_ex_order_status(order_num, status, notes):
    db.del_cache("exchange", order_num)
    return db.mysql.execute(
        "UPDATE `exchange_orders` SET `status` = %s, `notes` = %s "
        "WHERE `order_num` = %s", status, notes, order_num)

@db.db_cache("exchange")
def get_ex_order_ordernum(order_num):
    return db.mysql.get(
        "SELECT * FROM `exchange_orders` WHERE `order_num` = %s",
        order_num)

def get_ex_orders(uid):
    return db.mysql.query(
        "SELECT * FROM `exchange_orders` WHERE `uid` = %s ORDER BY `id` DESC LIMIT 50", uid)


@db.db_cache("exchange", count=0, ttl=300)
def count_exchange():
    data =  db.mysql.get(
        "SELECT sum(`face_price`) AS dsum FROM `exchange_orders` ")
    return data['dsum'] if data['dsum'] else 0
