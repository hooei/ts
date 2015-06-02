#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import tornado.web
import logging
import ujson as json
import utils
import urlparse
import base64
import constants
import session

from tornado.options import options
from models import users
from crypt import AESCipher

class BaseHandler(tornado.web.RequestHandler):
    """ 公共基础类 """

    def write_json(self, response=None):
        """Write json to client"""
        self.set_header('Content-type', 'application/json; charset=UTF-8')
        self.write(json.dumps(response))
        self.finish()

    def write_error(self, status_code, **kwargs):
        """Function to display custom error page defined in the handler.
        Over written from base handler."""

        reason = None
        err = constants.ERR_PROTOCOL_ERROR
        try:
            reason = kwargs['exc_info'][1].reason
            reason = reason if reason is not None \
                else kwargs['exc_info'][1].log_message
        except AttributeError or TypeError:
            err = constants.ERR_INTERNAL_ERROR

        if options.debug:
            logging.warning("Response err: %s" % reason)
            logging.warning("Request: %s" % self.request)
        if status_code == 404 or status_code == 500 :
            return self.render("error/error.html")
        self.return_error(err, reason)

    def return_success(self):
        self.write_json({"c": 0})

    def return_result(self, result={}):
        self.write_json({"c": 0, "d": result})

    def return_error(self, code, message=None):
        if not message:
            message = code[1]
        self.write_json({"c": code[0], "d": {}, "err": {'msg': message}})

    def return_error_bind(self, code):
        self.write_json({"c": code})

    @property
    def config(self):
        return self.application.config

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis


class WebBaseHandler(BaseHandler):
    """ Web基础类 """

    @property
    def session(self):
        session_params = {
            "secret": self.settings["session_secret"],
            "redis": self.redis,
            "timeout": 86400,
        }
        session_manager = session.SessionManager(**session_params)
        return session.Session(session_manager, self)

    @property
    def platform(self):
        user_agent = self.request.headers['User-Agent']
        return utils.get_platform(user_agent)

    def get_current_user(self):
        #ifa = self.session.get('ifa', None)
        oid = self.session.get('oid', None)
        # print `oid` +'oid'
        # print self.session
        if not oid:
            return None
        else:
            device = users.get_device(oid)
            if not device:
                return None
            user_info = users.get_info(device['uid'])
            user_info['oid'] = oid
            return user_info


class JSONBaseHandler(BaseHandler):
    """ Client基础类 """

    def decrypt_params(self, s):
        """ 解密参数 """
        # 约定:首部填充21字节随机字符
        s = base64.b64encode(base64.b64decode(s)[21:])
        aes = AESCipher(self.config['crypt']['aeskey'])
        decrypt_data = aes.decrypt(s.replace(' ', '+'))
        return dict([(k, v[0]) for k, v in urlparse.parse_qs(decrypt_data).items()])


