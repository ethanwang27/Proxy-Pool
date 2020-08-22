# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 14:00
@File: proxyHandler.py
@Project: Proxy-Pool
@Description: None
"""

from helper.proxyHelper import Proxy
from helper.mongoDbHelper import MongodbHelper


class ProxyHandler(object):

    def __init__(self):
        super(ProxyHandler, self).__init__()
        self.db = MongodbHelper()

    def get(self):
        """
        从DB中获取可用的代理
        :return:
        """
        proxy = self.db.get()
        if proxy:
            return Proxy(proxy)
        return None

    def pop(self):
        proxy = self.db.pop()
        if proxy:
            return Proxy.createFromJson(proxy)
        return None

    def put(self, proxy):
        self.db.put(proxy.proxy)

    def delete(self, proxy):
        return self.db.delete(proxy.proxy)

    def get_all(self):
        return [Proxy(proxy) for proxy in self.db.get_all()]

    def exits(self, proxy):
        return self.db.exists(proxy.proxy)

    def get_proxy_count(self):
        return {'count': self.db.get_proxy_count()}


if __name__ == '__main__':
    print(ProxyHandler().get())