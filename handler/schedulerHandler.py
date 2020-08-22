# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 16:16
@File: schedulerHandler.py
@Project: Proxy-Pool
@Description: None
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from queue import Empty, Queue

from helper.proxyHelper import Proxy
from helper.logHepler import LogHelper
from handler.fetcherHandler import run_fetcher
from handler.proxyCheckerHandler import run_checker
from handler.proxyHandler import ProxyHandler


def run_proxy_fetch():
    proxy_queue = Queue()

    for proxy in run_fetcher():
        proxy_queue.put(Proxy(proxy).to_json)

    run_checker('raw', proxy_queue)


def run_proxy_check():
    proxy_queue = Queue()

    for proxy in ProxyHandler().get_all():
        proxy_queue.put(proxy.to_json)
    run_checker('use', proxy_queue)


def run_scheduler():
    log = LogHelper("scheduler")
    log.info("scheduler start")

    scheduler = BlockingScheduler(logger=log)

    scheduler.add_job(run_proxy_fetch, 'interval', minutes=4, id="proxy_fetch", name="proxy采集")
    scheduler.add_job(run_proxy_check, 'interval', minutes=2, id="proxy_check", name="proxy检查")

    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=4)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

    scheduler.configure(executors=executors, job_defaults=job_defaults)
    scheduler.start()


if __name__ == '__main__':
    run_scheduler()
