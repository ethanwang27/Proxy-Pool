# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 18:39
@File: proxy_pool_interface.py
@Project: Proxy-Pool
@Description: None
"""
from abc import ABC

from werkzeug.wrappers import Response
from flask import Flask, jsonify, request
import gunicorn.app.base

from handler.proxyHandler import ProxyHandler
from helper.proxyHelper import Proxy

app = Flask(__name__)
proxy_handler = ProxyHandler()


class JsonResponse(Response):

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)
        return super(JsonResponse, cls).force_type(response, environ={} if environ is None else environ)


class StandaloneApplication(gunicorn.app.base.BaseApplication, ABC):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        _config = dict([(key, value) for key, value in self.options.items()
                        if key in self.cfg.settings and value is not None])
        for key, value in _config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


app.response_class = JsonResponse

api_list = {
    'get': u'获取一个proxy',
    'pop': u'获取一个proxy，并在数据库中删除',
    'get_all': u'获取数据库中的所有proxy',
    'delete?proxy=': u'删除指定proxy',
    'get_proxy_count': u'获取数据库中存书的proxy总数'
}


@app.route('/')
def index():
    return api_list


@app.route('/get/')
def get():
    proxy = proxy_handler.get()
    return proxy.proxy if proxy else {"code": 0, "src": "no proxy"}


@app.route('/pop/')
def pop():
    proxy = proxy_handler.pop()
    return proxy.proxy if proxy else {"code": 0, "src": "no proxy"}


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    status = proxy_handler.delete(Proxy(proxy))
    return {'code': 0, 'src': status}


@app.route('/get_proxy_count/')
def get_proxy_count():
    return proxy_handler.get_proxy_count()


def run_flask():
    _options = {
        'bind': 'localhost:8088',
        'workers': 4,
        'accesslog': '-',
        'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
    }

    StandaloneApplication(app, _options).run()


if __name__ == '__main__':
    run_flask()