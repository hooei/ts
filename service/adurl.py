#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

有米广告回调处理
 @author lisongjian@youmi.net

"""
import utils, datetime
from protocols import JSONBaseHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AdyoumiHandler(JSONBaseHandler):
    def get(self, platform):
        log_path = self.config['log']['adyoumi']
        utils.loggers.use('adyoumi', log_path).info(self.request.uri)
        self.__save_qianlu_order(platform)

    def __save_qianlu_order(self, platform):
        params = {}
        for key in ['ifa', 'mac', 'callback_url']:
            params[key] = self.get_argument(key, "")
        mac = params['mac'].encode('utf-8')
        idfa = params['ifa'].replace("-","").lower().encode('utf-8')
        if mac=='' and idfa=='':
            return self.write("{'c': -2, 'error':'parmas error'}")
        print params
        idfa_info = None
        if mac != '':
            idfa_info = self.db.get(
                "SELECT * FROM `wallad_clicks` WHERE `mac`=%s LIMIT 1",mac)

        if idfa !='':
            idfa_info = self.db.get(
                "SELECT * FROM `wallad_clicks` WHERE `idfa`=%s LIMIT 1",idfa)

        if not idfa_info:
            if platform == 'qianlu':
                adserver = 2
            elif platform == 'mopan':
                adserver = 25
            elif platform == 'qumi':
                adserver = 26
            elif platform == 'adw':
                adserver = 27
            elif platform == 'anwo':
                adserver = 41
                url = 'http://offer.adwo.com/iofferwallcharge/ia?adalias=qianlu'
                if mac:
                    url += '&uid=' + mac.upper()
                if idfa:
                    format_idfa = idfa[0:8]+'-'+idfa[8:12]+'-'+idfa[12:16]+'-'+idfa[16:20]+'-'+idfa[20:]
                    url += '&idfa=' + format_idfa.upper()
                params['callback_url'] = url
            self.db.execute(
                "INSERT INTO `wallad_clicks` (idfa, mac, callback_url, adserver,create_time)"
                "VALUES (%s, %s, %s, %s, %s)",
                idfa, mac, params['callback_url'], adserver, datetime.datetime.now())
            self.return_success()
        else:
            self.write("{'c': -1, 'error':'ready had idfa'}")
