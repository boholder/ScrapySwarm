#!/usr/bin/python3
'''
@File : unrepeated_db_insert_util.py

@Time : 2019/6/25

@Author : Boholder

@Function : 

'''

import pymongo


class UnrepeatedDBInsertUtil(object):
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
        self.bdsearch = db[COLL_BAIDU_SREACH]
        self.Information = db[COLL_WEIBO_INFOMATION]
        self.Tweets = db[COLL_WEIBO_TWEETS]
        self.Comments = db[COLL_WEIBO_COMMENTS]
        self.Relationships = db[COLL_WEIBO_RELATIONSHIPS]
        self.Chinanews = db[COLL_CHINA_NEWS]
        self.QQNews = db[COLL_QQ_NEWS]

    '''
    
    '''

    def NewsInsert