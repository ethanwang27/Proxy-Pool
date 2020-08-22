# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 11:47
@File: proxyFetcher.py
@Project: Proxy-Pool
@Description: None
"""

import time
from utils.WebRequest import WebRequest
from helper.logHepler import LogHelper

class ProxyFetcher(object):

    def __init__(self):
        super(ProxyFetcher, self).__init__()

    @staticmethod
    def get_kuaidaili_proxy(page_count=1):
        """
        获取快代理的高匿代理IP
        :param page_count:
        :return:
        """
        # 快代理的高匿代理URL
        url_pattern = 'https://www.kuaidaili.com/free/inha/{}/'
        url_list = []
        for page_index in range(1, page_count + 1):
            url_list.append(url_pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            time.sleep(2)
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0: 2])


if __name__ == '__main__':
    proxy_handler = ProxyFetcher()
    log = LogHelper("test")
    for item in proxy_handler.get_kuaidaili_proxy(2):
        log.info(item)
