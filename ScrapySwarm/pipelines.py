# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymongo
from pymongo.errors import DuplicateKeyError

from ScrapySwarm.tools.imag import download_pic
import ScrapySwarm.items as items
from ScrapySwarm.tools.unique_db_insert_util \
    import UniqueDBInsertUtil as Uni


class ScrapyswarmPipeline(object):
    uni = Uni()

    def __init__(self):
        from ScrapySwarm.settings import \
            LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, MONGO_DB_NAME, \
            COLL_BAIDU_SREACH, COLL_CHINA_NEWS, COLL_WEIBO_COMMENTS, \
            COLL_WEIBO_INFOMATION, COLL_WEIBO_RELATIONSHIPS, COLL_WEIBO_TWEETS, \
            COLL_QQ_NEWS, COLL_SINA_NEWS

        connection = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)

        db = connection[MONGO_DB_NAME]
        self.Bdsearch = db[COLL_BAIDU_SREACH]
        self.Information = db[COLL_WEIBO_INFOMATION]
        self.Tweets = db[COLL_WEIBO_TWEETS]
        self.Comments = db[COLL_WEIBO_COMMENTS]
        self.Relationships = db[COLL_WEIBO_RELATIONSHIPS]

        # # 新闻类已使用 UniqueDBInsertUtil 处理数据库操作
        # self.Chinanews = db[COLL_CHINA_NEWS]
        # self.QQNews = db[COLL_QQ_NEWS]
        # self.SinaNews = db[COLL_SINA_NEWS]

    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        # log.msg("Question added to MongoDB database!",
        #         level=log.DEBUG, spider=spider)

        if isinstance(item, items.BaiduSearchItem):
            self.insert_item(self.Bdsearch, item)
        elif isinstance(item, items.RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, items.TweetsItem):
            self.uni.weiboUniqueInsert(item)
        elif isinstance(item, items.InformationItem):
            self.insert_item(self.Information, item)
        elif isinstance(item, items.ChinaNewsItem):
            self.uni.newsUniqueInsert(item)
        elif isinstance(item, items.QQNewsItem):
            self.uni.newsUniqueInsert(item)
        elif isinstance(item, items.SinaNewsItem):
            self.uni.newsUniqueInsert(item)
        else :
            print('评论被保存')
            self.uni.commentsUniqueInsert(item)


        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            print("通过pipe插入")
            collection.insert(dict(item))
        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以
            pass