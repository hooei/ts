#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""验证码相关

"""

import tornado.web
import constants

from datetime import datetime
from protocols import WebBaseHandler
from modules import captcha

class SmsCaptchaHandler(WebBaseHandler):
    """ 发送短信验证码 """
    @tornado.web.authenticated
    def get(self):
        phone = str(self.get_argument('phone',""))
        if phone == "":
            return self.render('setting/phone.html')

        pkg = str(self.current_user['pkg'])
        flow = str(self.current_user['flow'])
        if pkg == "5" and flow == "1":
            if not phone.isdigit():
                return self.write(constants.ERR_PARAMS_NULL)
            else:
                err = captcha.check_freq_phone(phone)
                if err == False:
                    return self.return_error(constants.ERR_CAPTCHA_FREQUENCY)
            succ ,code = captcha.send_sms_ytx(phone, self.config['ytx'])
            if not succ:
                if code == '112314':
                    return self.return_error(constants.ERR_CAPTCHA_MANY)
                return self.return_error(constants.ERR_CAPTCHA_FAIL)
            else:
                key_name = "qianka:server:wait:%s" % phone
                self.redis.setex(key_name, 1, 60)
                key_name = "qianka:server:code:%s" % phone
                self.redis.setex(key_name, code, 600)
                self.return_success()

    @tornado.web.authenticated
    def post(self):
        # keys = ['phone', 'strs', 'ts']
        # params = {}
        # for key in keys:
        #     params[key] = self.get_argument(key, '')
        #     if not params[key]:
        #         return self.return_error(constants.ERR_PARAMS_NULL)
        # print params
        # if not params['phone'].isdigit():
        #     return self.return_error(constants.ERR_INVALID_PHONE)
        # # 检查图像验证码
        # err = captcha.check_pic(params['ts'], params['strs'])
        # if err:
        #     print err
        #     return self.return_error(err)

        # 不再需要图像验证码
        keys = ['phone']
        params = {}
        for key in keys:
            params[key] = self.get_argument(key, '')
            if not params[key]:
                return self.return_error(constants.ERR_PARAMS_NULL)
        print params
        if not params['phone'].isdigit():
            return self.return_error(constants.ERR_INVALID_PHONE)

        # 检查短信发送频率
        valid = captcha.check_freq_phone(params['phone'])
        if not valid:
            return self.return_error(constants.ERR_CAPTCHA_FREQUENCY)
        # 检查IP请求量 FIXME
        # 请求第三方发送短信
        succ, code = captcha.send_sms_ytx(params['phone'], self.config['ytx'])
        print succ, code
        if not succ:
            return self.return_error(constants.ERR_CAPTCHA_FAIL)
        else:
            key_name = "qianka:server:code:%s" % params['phone']
            self.redis.setex(key_name, code, 600)
            key_name = "qianka:server:wait:%s" % params['phone']
            self.redis.setex(key_name, 1, 120)
            return self.return_success()


class PicCaptchaHandler(WebBaseHandler):
    """ 获取图像验证码 """

    def get(self):
        ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_base64, strs = captcha.gen_pic_code()
        key_name = "qianka:pic:%s" % ts
        self.redis.setex(key_name, strs, 3600)
        self.return_result({"img": img_base64, "ts": ts})
