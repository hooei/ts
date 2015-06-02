#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

import db


def get(key):
    data = db.mysql.get(
        "SELECT * FROM `activity` WHERE `key` = %s", key)
    return data if data else 0

def get_prize():
	return db.mysql.query(
		"SELECT * FROM `prize`"
	)

def check_prize(uid,stime):
	return db.mysql.get(
		"SELECT count(*) as total FROM `prize_list` WHERE `uid` = %s AND `create_time` = %s", uid, stime
	)

def add_prize(uid, prize_id, money, create_time):
	return db.mysql.execute(
		"INSERT INTO `prize_list`(`uid`,`prize_id`,`money`,`create_time`) VALUES(%s, %s, %s, %s)",uid, prize_id, money,create_time
	)

def add_vip_task(parent_id, son_id):
	return db.mysql.execute(
		"INSERT INTO `vip_task`(`parent_id`, `son_id`) VALUES(%s, %s)", parent_id, son_id
	)

def count_vip_task(parent_id):
	return db.mysql.get(
		"SELECT count(*) as total FROM `vip_task` WHERE `parent_id` = %s", parent_id
	) 

