#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#
import urllib
import tornado.web
import torndb
import redis
import os.path
import server
import db
#import wsgiserver as server

from crypt import AESCipher
from protocols import WebBaseHandler
from service import user, duibaV2, invite, config, fun
from service import captcha, callback, client, adurl, crontab

try:
    import __pypy__
except ImportError:
    __pypy__ = None

class Application(server.Application):

    def startup(self):
        self.db = db.mysql = torndb.Connection(**self.config['mysql'])
        pool = redis.ConnectionPool(**self.config['redis'])
        self.redis = db.redis = redis.Redis(connection_pool=pool)


class MainHandler(WebBaseHandler):

    @tornado.web.authenticated
    def get(self):
        print self.current_user
        self.write("hello world!")


class TestHandler(tornado.web.RequestHandler):
    """ 测试 """

    def get(self):
        f = urllib.urlopen("http://www.google.com")
        print f

    def _encrypt_params(self, raw_params={}):
        aes = AESCipher(self.config['crypt']['aeskey'])
        s = []
        for k in raw_params:
            s.append(k + '=' + str(raw_params[k]))
        return aes.encrypt('&'.join(s))


class RequestHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404 or status_code ==500:
            self.render("error/error.html")


class PageNotFoundHandler(RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(404)
        self.render("/error/error.html")
tornado.web.ErrorHandler = PageNotFoundHandler



if __name__ == "__main__":
    static_path = os.path.join(os.path.dirname(__file__), "static")

    handlers = [
        (r'/static/(.*)',
            tornado.web.StaticFileHandler,
            {'path': static_path}),
        (r"/", user.WelcomeHandler),
        # 服务器维护拦截
        #(r"/.*", user.WelcomeHandler),

        # 客户端请求操作
        # 用户登陆接口
        (r"/login", client.LoginHandler),
        # 客户端积分轮询
        (r"/getmsg", client.GetMsgHandler),

        # 钱鹿登陆接口
        (r"/welcome", user.WelcomeHandler),
        (r"/islogin", user.IsLoginHandler),
        (r"/logout", user.LogoutHandler),

        # 定时器
        (r"/crontab/save_channel_click", crontab.ChannelHandler),
        (r"/crontab/resend_anwo", crontab.AnwoHandler),

        # 用户主页页面
        (r"/home", user.HomeHandler),
        # 用户等级
        (r"/level",user.LevelHandler),
        # 用户明细页面
        (r"/detail", user.DetailHandler),

        # 用户资料
        (r"/info", user.InfoHandler),
        (r"/info/headimg", user.HeadimgHandler),
        # 绑定手机
        (r"/phone", user.PhoneHandler),
        (r"/phone/unlock", user.PhoneUnlockHandler),
        (r"/getid", user.GetIDHandler),
        (r"/switch", user.SwitchHandler),

        # 任务
        (r"/task", user.TaskHandler),
        (r"/union", user.UnionHandler),
        (r"/task/teach", user.TeachHandler),
        (r"/task/video", user.TaskVideoHandler),
        (r"/task/survey", user.TaskSurveyHandler),

        # 每日抽奖
        (r"/fun/lottery", fun.LotteryHandler),

        # 收徒
        (r"/invite", invite.MyInviteHandler),
        # 分享
        (r"/share", invite.ShareHandler),
        # 我的名片
        (r"/card", invite.CardHandler),


        #下载接口
        (r"/ipa/latest", invite.DownloadHandler),
        # 设置
        (r"/config", config.ConfigHandler),
        # 意见反馈
        (r"/feedback", config.FeedbackHandler),
        # 常见问题
        (r"/faq", config.FAQHandler),
        # 联系我们
        (r"/contact", config.ContactHandler),

        # 图像验证码
        (r"/pic", captcha.PicCaptchaHandler),
        (r"/code", captcha.SmsCaptchaHandler),
        #(r"/code", user.PhoneHandler),
        # 广告回调
        (r"/callback/([^/]+)", callback.CallbackHandler),
        #米禾回调
        (r"/callback", callback.MiheCallbackHandler),
        # 兑换
        (r"/exchange", duibaV2.LoginHandler),
        (r"/duiba/consume", duibaV2.ConsumeHandler),
        (r"/duiba/notify", duibaV2.NotifyHandler),
        # youmi广告回调
        (r"/ad/([^/]+)/.+", adurl.AdyoumiHandler),

        # 测试
        (r"/test", TestHandler),
        # 错误页面
        (r".*", PageNotFoundHandler),
    ]

    server.mainloop(Application(handlers))
