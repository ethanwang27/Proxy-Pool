# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/15 20:41
@File: mongoDbHelper.py
@Project: Proxy-Pool
@Description: None
"""

from pymongo import MongoClient
import config


class MongodbHelper(object):

    def __init__(self):
        self.name = config.DB_COLLECTION
        self.client = MongoClient(config.DB_HOST, config.DB_PORT)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.DB_COLLECTION]

    def get(self):
        data = self.collection.find_one({})
        return data['proxy'] if data is not None else None

    def put(self, proxy):
        if self.collection.find_one({'proxy': proxy}):
            return None
        else:
            self.collection.insert_one({'proxy': proxy})

    def pop(self):
        data = list(self.collection.aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            value = data['proxy']
            self.delete(value)
            return {'proxy': value}
        return None

    def delete(self, value):
        return self.collection.delete_one({'proxy': value}).deleted_count

    def delete_all(self):
        return self.collection.delete_many({}).deleted_count

    def get_all(self):
        return {p['proxy'] for p in self.collection.find()}

    def update(self, key, value):
        return self.collection.update({'proxy': key}, {'$inc': {'port': value}})

    def exists(self, key):
        return True if self.collection.find_one({'proxy': key}) is not None else False

    def get_proxy_count(self):
        return self.collection.count()


if __name__ == '__main__':
    db = MongodbHelper()
    # print(db.put('192.168.98.78', 8909))
    db.put('192.68.89.67', 9866)
    # print(db.pop())
