# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 11:48
@File: proxyHelper.py
@Project: Proxy-Pool
@Description: None
"""

import json
from helper.logHepler import LogHelper


class Proxy(object):

    def __init__(self, proxy, fail_count=0, region='', proxy_type='',
                 source='', check_count=0, last_status='', last_time=''):
        self._proxy = proxy
        self._fail_count = fail_count
        self._region = region
        self._proxy_type = proxy_type
        self._source = source
        self._check_count = check_count
        self._last_status = last_status
        self._last_time = last_time

    @classmethod
    def createFromJson(cls, proxy_json):
        proxy_dict = json.loads(proxy_json)
        return cls(proxy=proxy_dict.get("proxy", ""),
                   fail_count=proxy_dict.get("fail_count", 0),
                   region=proxy_dict.get("region", ""),
                   proxy_type=proxy_dict.get("proxy_type", ""),
                   source=proxy_dict.get("source", ""),
                   check_count=proxy_dict.get("check_count", 0),
                   last_status=proxy_dict.get('last_status', ""),
                   last_time=proxy_dict.get('last_time', '')
                   )

    @property
    def proxy(self):
        return self._proxy

    @property
    def fail_count(self):
        return self._fail_count

    @property
    def region(self):
        return self._region

    @property
    def proxy_type(self):
        return self._proxy_type

    @property
    def source(self):
        return self._source

    @property
    def check_count(self):
        return self._check_count

    @property
    def last_status(self):
        return self._last_status

    @property
    def last_time(self):
        return self._last_time

    @property
    def get_proxy_dict(self):
        return {'proxy': self._proxy,
                'fail_count': self._fail_count,
                'region': self._region,
                'proxy_type': self._proxy_type,
                'source': self._source,
                'check_count': self._check_count,
                'last_status': self._last_status,
                'last_time': self._last_time}

    @property
    def to_json(self):
        """ 属性json格式 """
        return json.dumps(self.get_proxy_dict, ensure_ascii=False)

    # --- proxy method ---
    @fail_count.setter
    def fail_count(self, value):
        self._fail_count = value

    @region.setter
    def region(self, value):
        self._region = value

    @proxy_type.setter
    def proxy_type(self, value):
        self._proxy_type = value

    @source.setter
    def source(self, value):
        self._source = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value


if __name__ == '__main__':
    print(Proxy('171.35.149.74:9999').to_json)