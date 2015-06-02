#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import os.path

""" Tornado Server 定义 """
# 接收到关闭信号后多少秒后才真正重启
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
# Listen IPV4 only
IPV4_ONLY = True

""" 全局配置常量 """
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

PLATFORM_UNKNOWN = 0
PLATFORM_ANDROID = 1
PLATFORM_IOS = 2

SETTINGS_FILE = "settings.yaml"

""" 协议相关 """
ERR_PROTOCOL_ERROR = (-1001, "协议解析错误")
ERR_INTERNAL_ERROR = (-1002, "内部错误")
ERR_DECRYPT_FAIL = (-1003, "解密失败")
ERR_PARAMS_NULL = (-1004, "参数不能为空")

""" 验证相关 """
ERR_CAPTCHA_INVALID = (-2001, "验证码无效")
ERR_CAPTCHA_ERROR = (-2002, "验证码错误")
ERR_CAPTCHA_FREQUENCY = (-2003, "验证码发送频繁")
ERR_CAPTCHA_FAIL = (-2004, "验证码发送失败")

""" 手机号码相关 """
ERR_INVALID_PHONE = (-3001, "手机号码非法")

""" 邀请相关 """
ERR_IVCODE_INVALID = (-4001, "邀请码无效")

""" 用户相关 """
ERR_NO_LOGIN = (-5001, "用户未登录")
ERR_BIND_FAIL = (-5002, "绑定用户失败")
ERR_MD5IFA_FAIL = (-5003, "MD5IFA重复")

""" 兑换相关 """
ERR_KEY_NOT_MATCH = (-6001, 'AppKey不匹配')
ERR_TIME_NOT_NULL = (-6002, '时间戳不能为空')
ERR_INVALID_TIME = (-6003, '时间戳无效')
ERR_INVALID_SIGN = (-6004, '签名验证失败')

""" 抽奖相关 """
ERR_INVALID_TIME = (-1, '今日抽奖次数用完')
ERR_INVALID_DATE = (-1, '今日抽奖次数用完')
