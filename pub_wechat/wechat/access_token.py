# -*- coding: utf-8 -*-
# filename: basic.py
import urllib.request
import time
import json
import threading


class AccessTokenManager:
    def __init__(self, appId, app_secrete):
        self.__access_token = ''
        self.__left_time = 0
        self.appId = appId
        self.app_secrete = app_secrete
        self.lock = threading.Lock()

    def __real_get_access_token(self):
        self.lock.acquire() 
        try:
          postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                    "client_credential&appid=%s&secret=%s" % (self.appId, self.app_secrete))
          with urllib.request.urlopen(postUrl) as urlResp:
                data = json.loads(urlResp.read().decode())

                print("==========\n Acquire Access Token: \n", data, "\n ===========\n")

                self.__access_token = data['access_token']
                self.__left_time = data['expires_in']
        finally:
            self.lock.release()


    def get_access_token(self):
        if self.__left_time < 10:
            self.__real_get_access_token()
        return self.__access_token

    
    def run(self):
        while(True):
            if self.__left_time > 10:
                time.sleep(3)
                self.__left_time -= 3
            else:
                self.__real_get_access_token()
