#!/usr/bin/python3
'''
@File : unique_db_insert_util.py

@Time : 2019/6/25

@Author : Boholder

@Function : 

'''

import pymongo
import ScrapySwarm.items as items


class UniqueDBInsertUtil(object):
    '''
    初始化，连接数据库之类
    '''

    def __init__(self):
        from ScrapySwarm.settings import \
            LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, MONGO_DB_NAME, \
            COLL_BAIDU_SREACH, COLL_CHINA_NEWS, COLL_WEIBO_COMMENTS, \
            COLL_WEIBO_INFOMATION, COLL_WEIBO_RELATIONSHIPS, COLL_WEIBO_TWEETS, \
            COLL_QQ_NEWS

        connection = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)

        db = connection[MONGO_DB_NAME]
        self.Bdsearch = db[COLL_BAIDU_SREACH]
        self.Information = db[COLL_WEIBO_INFOMATION]
        self.Tweets = db[COLL_WEIBO_TWEETS]
        self.Comments = db[COLL_WEIBO_COMMENTS]
        self.Relationships = db[COLL_WEIBO_RELATIONSHIPS]
        self.Chinanews = db[COLL_CHINA_NEWS]
        self.QQNews = db[COLL_QQ_NEWS]

        # create news collection unique index
        field=[
            ("url", pymongo.DESCENDING),
            ("time", pymongo.ASCENDING)
        ]
        self.Chinanews.create_index(field, unique= True )
        self.QQNews.create_index(field, unique= True)

        # 剩下的你对照着加吧，你那个weibo可能因为爬取类型不同，要写不只一个索引
        # 索引是对应单个集合的，
        # 所以实际上我上面那个没必要两个新闻统一一个索引

        # weibo collection unique index
        field={
            "1": 1
        }


    '''
    
    '''

    def newsUniqueInsert(self, item):
        if isinstance(item, items.ChinaNewsItem):
            self.Chinanews.insert(dict(item))
        elif isinstance(item, items.QQNewsItem):
            self.QQNews.insert(dict(item))