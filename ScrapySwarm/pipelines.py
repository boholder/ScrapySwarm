# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

import ScrapySwarm.items as items
from ScrapySwarm.control.DBAccess \
    import UniqueDBInsertUtil as Uni
from ScrapySwarm.control.DBAccess \
    import NormalDBInsertUtil as Nor


class ScrapyswarmPipeline(object):
    uni = Uni()
    nor = Nor()

    def __init__(self):
        from ScrapySwarm.settings import \
            LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, MONGO_DB_NAME, \
            COLL_BAIDU_SREACH, COLL_WEIBO_COMMENTS, \
            COLL_WEIBO_INFOMATION, COLL_WEIBO_RELATIONSHIPS, COLL_WEIBO_TWEETS

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
            self.nor.insert_item( item)
        elif isinstance(item, items.RelationshipsItem):
            self.nor.insert_item( item)
        elif isinstance(item, items.TweetsItem):
            self.uni.weiboUniqueInsert(item)
        elif isinstance(item, items.InformationItem):
            self.nor.insert_item( item)
        elif isinstance(item, items.ChinaNewsItem):
            self.uni.newsUniqueInsert(item)
        elif isinstance(item, items.QQNewsItem):
            self.uni.newsUniqueInsert(item)
        elif isinstance(item, items.SinaNewsItem):
            self.uni.newsUniqueInsert(item)
        elif isinstance(item, items.CommentItem):
            self.uni.commentsUniqueInsert(item)
        else:
            self.nor.insert_item( item)
        return item
