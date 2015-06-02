#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: luojianqiang@youmi.net
#

"""定时器相关

"""
import utils
import urllib2
from protocols import WebBaseHandler
from models import channel_clicks, wallad_clicks

class ChannelHandler(WebBaseHandler):
    """ 将redis的渠道点击数据同步到数据库"""

    def post(self):
        # TODO 安全起见，只能允许服务器内部调用，需要添加过滤规则
        #host = self.request.headers['Host']

        # 由于数据库中不存在id为0的值，特殊处理
        v = self.redis.get("qianka:channel_click:0")
        channel_clicks.init_today(0)
        if v:
            self.redis.set("qianka:channel_click:0",0)
            channel_clicks.increase_click(0, v)
            utils.loggers.use('channel_click', self.config['log']['channel_click']).info('save channel:0 '+ v)
        self.redis.set("qianka:channel_click:0",0)


        # 渠道点击统计,通过脚本将redis中的数据同步到数据库，每小时执行一次
        channel_ids = channel_clicks.get_all_channel_ids()
        for channel_id in channel_ids:
            cne = str(channel_id['id'])
            value = self.redis.get("qianka:channel_click:"+cne)
            # 如果数据库中还没有今天的数据则初始化之
            channel_clicks.init_today(cne)
            if value:
                self.redis.set("qianka:channel_click:"+cne,0)
                channel_clicks.increase_click(cne, value)
                utils.loggers.use('channel_click', self.config['log']['channel_click']).info('save channel:'+cne+' '+value)
            self.redis.set("qianka:channel_click:"+cne,0)


        utils.loggers.use('channel_click', self.config['log']['channel_click']).info("channel save")


class AnwoHandler(WebBaseHandler):
    """ """

    def post(self):
        # TODO 安全起见，只能允许服务器内部调用，需要添加过滤规则
        #host = self.request.headers['Host']

        keys = self.redis.keys("qianka:anwo:failed:*")
        for key in keys:
            ttl = self.redis.ttl(key)
            print type(ttl),ttl
            if ttl % 3600 <= 60:
                wallad_id = self.redis.get(key)
                try:
                    wallad_click = wallad_clicks.get_by_id(wallad_id)
                    if wallad_click and wallad_click.status != 1:
                        msg = str(urllib2.urlopen(wallad_click.callback_url).read())
                        wallad_clicks.update(msg, wallad_id)
                        wallad_clicks.set_user_pkg(wallad_click.uid, wallad_click.adserver)
                        self.redis.delete(key)
                        utils.loggers.use('adyoumi', self.config['log']['adyoumi']).info("[anwo success] "+ key)
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                    utils.loggers.use('adyoumi', self.config['log']['adyoumi']).info("[anwo error] "+ msg)
                    if ttl <= 60:
                        self.redis.delete(key)
                        wallad_clicks.delete_by_id(wallad_id)
                        utils.loggers.use('adyoumi', self.config['log']['adyoumi']).info("[anwo delete] "+ key)
