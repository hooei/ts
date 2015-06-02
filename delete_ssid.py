#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author chenjiehua@youmi.net
#

import yaml
import torndb
import redis
import db

from utils import YamlLoader

SETTINGS_FILE = "settings.yaml"

try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

pool = redis.ConnectionPool(**config['redis'])
db.redis = redis.Redis(connection_pool=pool)
db.mysql = torndb.Connection(**config['mysql'])

def main():
    devices = db.mysql.query("SELECT * FROM `devices`")
    for d in devices:
        ssid = db.redis.get(d['oid'])
        if not ssid:
            continue
        print d['oid'], ssid
        db.redis.delete(ssid)


if __name__ == "__main__":
    main()
