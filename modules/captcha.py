#!/usb/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author chenjiehua@youmi.net
#

import random
import base64
import requests
import ujson as json
import constants
import utils
import db

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from StringIO import StringIO
from datetime import datetime

def check_pic(ts, strs):
    """ 验证图像验证码 """
    key_name = "qianka:pic:%s" % ts
    data = db.redis.get(key_name)
    if not data:
        msg = constants.ERR_CAPTCHA_INVALID
    elif str(strs).upper() != str(data).upper():
        msg = constants.ERR_CAPTCHA_ERROR
    else:
        msg = None
    db.redis.delete(key_name)
    return msg


def check_sms(phone, code):
    """ 验证短信验证码 """
    key_name = "qianka:server:code:%s" % phone
    data = db.redis.get(key_name)
    if not data:
        msg = constants.ERR_CAPTCHA_INVALID
    elif int(code) != int(data):
        msg = constants.ERR_CAPTCHA_ERROR
    else:
        msg = None
        db.redis.delete(key_name)
    return msg


def check_freq_phone(phone):
    """ 检验请求发送频率 """
    key_name = "qianka:wait:%s" % phone
    if db.redis.get(key_name):
        return False
    return True


def check_freq_ip(ip):
    """ 检验单个IP发送数量 """
    pass


def gen_pic_code(size=(120, 30),
                img_type="GIF",
                mode="RGB",
                bg_color=(255, 255, 255),
                fg_color=(0, 0, 255),
                font_size=22,
                font_type="ubuntu.ttf",
                length=4,
                draw_lines=True,
                n_line=(1, 2),
                draw_points=True,
                point_chance=2):
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    :q
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''
    width, height = size
    img = Image.new(mode, size, bg_color) # 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔
    font_type = constants.STATIC_DIR + '/' + font_type

    _letter_cases = "abcdefghijklmnopqrstuvwxyz" # 小写字母，去除可能干扰的i，l，o，z
    _upper_cases = _letter_cases.upper() # 大写字母
    _numbers = ''.join(map(str, range(0, 10))) # 数字
    chars = ''.join((_letter_cases, _upper_cases, _numbers))

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line) # 干扰线条数
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            #结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()

    strs = create_strs()
    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
            ]
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）
    output = StringIO()
    img.save(output, 'PNG')
    img_data = output.getvalue()
    output.close()
    img_base64 = base64.encodestring(img_data)
    return img_base64, strs


def send_sms_ytx(phone, ytx):
    """ 容联云通讯短信验证码 """
    # FIXME 修改为异步 or 消息队列
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    sig = utils.md5(ytx['acid'] + ytx['actoken'] + ts).upper()
    url = '%s/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % \
        (ytx['url'], ytx['acid'], sig)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": base64.b64encode(ytx['acid'] + ':' + ts),
    }
    code = str(random.randint(100000, 999999))
    payload = {
        "to": phone,
        "appId": ytx['appid'],
        #"templateId": "18791",
        "templateId": "19557",
        "datas": [code, '10'],
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    result = r.json()
    print result
    if result['statusCode'] == '000000':
        return True, code
    else:
        return False, None


def send_sms_tui3(phone, tui3):
    """ 推立方短信验证码 """
    code = random.randint(10000, 99999)
    apikey = tui3['apikey']
    url = "http://tui3.com/api/code/?k=%s&t=%s&c=%s&ti=1" \
        % (apikey, phone, code)
    req = requests.get(url)
    result = req.json()
    if result['err_code'] == 0:
        return True, code
    else:
        return False, None

