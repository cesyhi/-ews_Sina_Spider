# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient
from scrapy.conf import settings
import redis


class NewssinaPipeline(object):

    def __init__(self):

        self.file = open('news_sina.json', 'w')

    def process_item(self, item, spider):
        self.file.write(item['content'])
        return item

    def closespider(self):
        self.file.close()


class SinaPipeline(object):

    def process_item(self, item, spider):
        sonUrls = item['sonUrl']
        print("8888888888888888888888888888888888888888888888888888888")
        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = sonUrls[7:-6].replace('/', '_')
        filename += ".txt"

        fp = open(item['subFilename']+'/'+filename, 'w')
        fp.write(item['content'])
        fp.close()

        return item



class MonogoPipeline(object):

    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbs = settings['MONGO_DB']
        cline = settings['MONGO_CLINE']

        # 创建链接
        self.heaned = MongoClient(host=host, port=port)
        self.data = self.heaned[dbs]
        self.cli = self.data[cline]

    def process_item(self, item, spider):
        print("=========================================================")
        # print(type(item))
        # result = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        result = dict(item)
        self.cli.insert(result)
        return item

    def closespider(self):
        self.heaned.close()
