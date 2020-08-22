# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 14:54
@File: fetcherHandler.py
@Project: Proxy-Pool
@Description: None
"""

from helper.logHepler import LogHelper
from handler.proxyHandler import ProxyHandler
from fetcher.proxyFecther import ProxyFetcher
import config


class FetcherHandler(object):

    def __init__(self):
        self.name = 'fetcherHandler'
        self.log = LogHelper(self.name)
        self.proxy_handler = ProxyHandler()

    def fetcher(self):
        proxy_set = set()
        self.log.info(self.name + ": start")
        for fetcher_name in config.PROXY_FETCHER_LIST:
            self.log.info(self.name + " {}: start".format(fetcher_name))
            fetcher = getattr(ProxyFetcher, fetcher_name, None)
            if not fetcher:
                self.log.error("ProxyFetcher {} not exists".format(fetcher_name))
                continue
            if not callable(fetcher):
                self.log.error("ProxyFetcher {} must be class method".format(fetcher_name))
                continue

            try:
                for proxy in fetcher():
                    proxy = proxy.strip()
                    if len(proxy) == 0:
                        continue
                    if proxy in proxy_set:
                        self.log.info(self.name + " {}: {} exists".format(fetcher_name, proxy.ljust(20)))
                        continue
                    else:
                        self.log.info(self.name + " {}: {} success".format(fetcher_name, proxy.ljust(20)))
                        proxy_set.add(proxy)
            except Exception as e:
                self.log.error(self.name + " {}: error! \n{}".format(fetcher_name, str(e)))
            self.log.info(self.name + " run complete!")
            return proxy_set


def run_fetcher():
    return FetcherHandler().fetcher()


if __name__ == '__main__':
    print(FetcherHandler().fetcher())

