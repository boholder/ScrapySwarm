# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymongo
from pymongo.errors import DuplicateKeyError
from  ScrapySwarm.tools.imag import download_pic
import ScrapySwarm.items as items


class ScrapyswarmPipeline(object):

    def __init__(self):
        from ScrapySwarm.settings import LOCAL_MONGO_HOST,LOCAL_MONGO_PORT,MONGO_DB_NAME,COLL_BAIDU_SREACH,COLL_CHINA_NEWS,COLL_WEIBO_COMMENTS,COLL_WEIBO_INFOMATION,COLL_WEIBO_RELATIONSHIPS,COLL_WEIBO_TWEETS
        connection = pymongo.MongoClient(LOCAL_MONGO_HOST,LOCAL_MONGO_PORT)
        db = connection[MONGO_DB_NAME]
        self.bdsearch = db[COLL_BAIDU_SREACH]
        self.Information = db[COLL_WEIBO_INFOMATION]
        self.Tweets = db[COLL_WEIBO_TWEETS]
        self.Comments = db[COLL_WEIBO_COMMENTS]
        self.Relationships = db[COLL_WEIBO_RELATIONSHIPS]
        self.Chinanews = db[COLL_CHINA_NEWS]

    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        # log.msg("Question added to MongoDB database!",
        #         level=log.DEBUG, spider=spider)

        if isinstance(item, items.BaiduSearchItem):
            self.insert_item(self.bdsearch, item)
        elif isinstance(item, items.RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, items.TweetsItem):
            self.insert_item(self.Tweets, item)
        elif isinstance(item, items.InformationItem):
            self.insert_item(self.Information, item)
        elif isinstance(item, items.CommentItem):
            self.insert_item(self.Comments, item)
        elif isinstance(item, items.ChinaNewsItem):
            self.insert_item(self.Chinanews, item)
            for img in item['imgs']:
                image_path1=img.split("/")[-1]
                image_path1=item["url"].split("/")[-1]+image_path1
                image_path = os.path.join("e:china",image_path1)
                download_pic(img, image_path)
        return item

    @staticmethod
    def insert_item(collection, item):

        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            # 有重复数�
            pass
