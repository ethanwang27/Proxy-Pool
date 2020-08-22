# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 14:04
@File: config.py
@Project: Proxy-Pool
@Description: None
"""

# mongoDB 连接
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "proxy_pool"
DB_COLLECTION = "proxy_pool"


MAX_FAIL_COUNT = 3

PROXY_FETCHER_LIST = ['get_kuaidaili_proxy']

