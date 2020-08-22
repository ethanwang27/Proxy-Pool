# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 12:47
@File: proxyCheckerHandler.py
@Project: Proxy-Pool
@Description: None
"""

from threading import Thread
from datetime import datetime

from helper.logHepler import LogHelper
from helper.proxyHelper import Proxy
from utils.proxy_validators import validators
from handler.proxyHandler import ProxyHandler

import config


def check_proxy(proxy_obj):
    def __check_proxy(proxy):
        for func in validators:
            if not func(proxy):
                return False
        return True

    if __check_proxy(proxy_obj.proxy):
        proxy_obj.check_count += 1
        proxy_obj.last_status = 1
        proxy_obj.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if proxy_obj.fail_count > 0:
            proxy_obj.fail_count -= 1
    else:
        proxy_obj.check_count += 1
        proxy_obj.last_status = 0
        proxy_obj.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proxy_obj.fail_count += 1
    return proxy_obj


class Checker(Thread):

    def __init__(self, check_type, queue, thread_name):
        Thread.__init__(self, name=thread_name)
        self.type = check_type
        self.log = LogHelper("proxy_checker")
        self.proxy_handler = ProxyHandler()
        self.queue = queue

    def run(self) -> None:
        self.log.info("ProxyCheck - {} : start".format(self.name))
        while True:
            try:
                proxy_json = self.queue.get(block=False)
            except Exception:
                self.log.info("ProxyCheck - {} : complete".format(self.name))
                break

            proxy = Proxy.createFromJson(proxy_json)
            proxy = check_proxy(proxy)
            if self.type == "raw":
                if proxy.last_status:
                    if self.proxy_handler.exits(proxy):
                        self.log.info("ProxyCheck - {} : {} exits".format(self.name, proxy.proxy.ljust(23)))
                    else:
                        self.log.info("ProxyCheck - {} : {} success".format(self.name, proxy.proxy.ljust(23)))
                        self.proxy_handler.put(proxy)
                else:
                    self.log.info("ProxyCheck - {} : {} fail".format(self.name, proxy.proxy.ljust(23)))
            else:
                if proxy.last_status:
                    self.log.info("ProxyCheck - {} : {} pass".format(self.name, proxy.proxy.ljust(23)))
                    self.proxy_handler.put(proxy)
                else:
                    if proxy.fail_count > config.MAX_FAIL_COUNT:
                        self.log.info("ProxyCheck - {} : {} fail, count {} delete".format(self.name,
                                                                                          proxy.proxy.ljust(23),
                                                                                          proxy.fail_count))
                        self.proxy_handler.delete(proxy)
                    else:
                        self.log.info("ProxyCheck - {} : {} fail, count {} keep".format(self.name,
                                                                                        proxy.proxy.ljust(23),
                                                                                        proxy.fail_count))
                        self.proxy_handler.put(proxy)
            self.queue.task_done()


def run_checker(proxy_type, queue):
    thread_list = []
    for index in range(5):
        thread_list.append(Checker(proxy_type, queue, 'thread_%s' % str(index).zfill(2)))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
