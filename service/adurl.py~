#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

有米广告回调处理
 @author lisongjian@youmi.net

"""
import utils, hashlib, datetime
from protocols import JSONBaseHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AdyoumiHandler(JSONBaseHandler):
    def get(self, platform):
        log_path = self.config['log']['adyoumi_log']
        utils.print_log('adyoumi', log_path, self.request.uri)
        if platform == 'adyoumi':
            self.__save_adyoumi_order()
        elif platform == 'iosadyoumi':
            self.__save_iosadyoumi_order()
        elif platform == 'tapjoy':
            self.__save_tapjoy_order()
        elif platform == 'adxmi':
            self.__save_adxmi_order()
        elif platform == 'fb':
            self.__save_fb_order()

    def __save_adyoumi_order(self):
        params = {}
        for key in ['imei', 'imsi', 'android_id', 'mac', 'callback_url']:
            params[key] = self.get_argument(key, "")
        ei = params['imei'].encode('utf-8')
        si = params['imsi'].encode('utf-8')
        if si == '':
            si = 'null'
        mac = params['mac'].encode('utf-8')
        andid = params['android_id'].encode('utf-8')
        token = self.__get_devicefingerprinting(ei,si,mac,andid)
        #print token
        token_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `token`=%s LIMIT 1",token)
        if not token_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (imei, imsi, mac, andid, token,callback_url, adserver,create_time)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                ei, si, mac, andid, token, params['callback_url'], 1, datetime.datetime.now())
            self.return_success()
        else:
            self.write('already had token')

    def __save_adxmi_order(self):
        params = {}
        for key in ['imei', 'imsi', 'android_id', 'mac', 'callback_url']:
            params[key] = self.get_argument(key, "")
        ei = params['imei'].encode('utf-8')
        si = params['imsi'].encode('utf-8')
        if si == '':
            si = 'null'
        mac = params['mac'].encode('utf-8')
        andid = params['android_id'].encode('utf-8')
        token = self.__get_devicefingerprinting(ei,si,mac,andid)
        #print token
        token_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `token`=%s LIMIT 1",token)
        if not token_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (imei, imsi, mac, andid, token,callback_url, adserver,create_time)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                ei, si, mac, andid, token, params['callback_url'], 3, datetime.datetime.now())
            self.return_success()
        else:
            self.write('already had token')

    def __save_iosadyoumi_order(self):
        params = {}
        for key in ['ifa', 'mac', 'callback_url']:
            params[key] = self.get_argument(key, "")
        mac = params['mac'].encode('utf-8')
        idfa = params['ifa'].encode('utf-8')
        #print token
        idfa_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `idfa`=%s LIMIT 1",idfa)
        if not idfa_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (idfa, mac, callback_url, adserver,create_time)"
                "VALUES (%s, %s, %s, %s, %s)",
                idfa, mac, params['callback_url'], 1, datetime.datetime.now())
            self.return_success()
        else:
            self.write('already had idfa')

    def __save_tapjoy_order(self):
        params = {}
        for key in ['mac', 'idfa', 'source']:
            params[key] = self.get_argument(key, "")
        url = 'http://play.google.com/store/apps/details?id=net.ym.overseas.cashbox'
        self.redirect(url)
        ad_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `advertising_id`=%s AND `adserver`=2 LIMIT 1", params['idfa'])
        if not ad_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (advertising_id, mac, adserver,create_time)"
                "VALUES (%s, %s, %s, %s)",
                params['idfa'], params['mac'], 2, datetime.datetime.now())

    def __save_fb_order(self):
        url = 'http://play.google.com/store/apps/details?id=net.ym.overseas.cashbox'
        self.redirect(url)
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ad_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `ip`=%s AND `adserver`=4 LIMIT 1", ip)
        if not ad_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (ip, adserver,create_time)"
                "VALUES (%s, %s, %s)",
                ip, 2, datetime.datetime.now())


    def __get_devicefingerprinting(self, ei, si, mac, andid ):
        """简单的生成设备指纹方法"""
        valid_params = [
            ei,
            si,
            mac,
            andid,
        ]
        device_str = ':'.join(str(valid_params))
        #print device_str
        return hashlib.md5(device_str).hexdigest()

