#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenyongjian@youmi.net
#

"""新手任务"""

import db

def new_task_ios(uid, task_id):
    return db.mysql.execute(
        "INSERT INTO `user_task_ios`(`uid`, `task_id`) VALUES(%s, %s)",uid, task_id
    )
    
def check_task_ios(uid, task_id):
	return db.mysql.get(
		"SELECT count(`id`) AS total FROM `user_task_ios` WHERE `uid` = %s AND `task_id` = %s", uid, task_id
	)

def first_task_ios(uid):
	return db.mysql.get(
		"SELECT count(`id`) AS total FROM `user_task_ios` WHERE `uid` = %s ", uid
	)
