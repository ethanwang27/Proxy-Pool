# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 12:54
@File: proxy_validators.py
@Project: Proxy-Pool
@Description: None
"""

import requests
import re

validators = []


def validator(func):
    validators.append(func)
    return func


@validator
def format_validator(proxy):
    regex = r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5]):\d{0,5}'
    _proxy = re.findall(regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@validator
def timeout_validator(proxy):

    proxies = {'http': "http://{proxy}".format(proxy=proxy),
               'https': f"https://{proxy}".format(proxy=proxy)}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    try:
        response = requests.head("http://www.baidu.com", headers=headers,
                                 proxies=proxies, timeout=20)
        if response.status_code == 200:
            return True
    except Exception as e:
        pass
    return False


if __name__ == '__main__':
    print(timeout_validator("117.186.49.50:55443"))