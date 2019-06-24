#!/usr/bin/python3
# encoding: utf-8
'''
@File : bdsearch_url_util.py

@Time : 2019/6/23

@Author : Boholder

@Function : 从MongoDB拉取，由百度爬虫爬下的目标网站的文章的url，
            生成列表并返回。
            爬虫结束时
            该模块被其他需要借助百度搜索提供url的爬虫们调用。

'''

import pymongo



class BDsearchUrlUtil(object):
    '''
    初始化，连接数据库之类
    '''

    def __init__(self):
        from ScrapySwarm.settings import \
            LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, MONGO_DB_NAME, \
            COLL_BAIDU_SREACH
        connection = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = connection[MONGO_DB_NAME]
        self.bdsearch = db[COLL_BAIDU_SREACH]

    '''
    从mongodb中按'site'表项读取所有“新的('waste'=0)”url,
    组成url列表并返回列表
    
    @ param {string} site   exm: 'news.qq.com'
    
    @ return {List|None}  [url1,url2,url3,...] 
                            urlexm: 'http://baidu.com/...'
                          None for no new url
    '''

    def getNewUrl(self, site):
        # construct query and fliter
        query = {
            "site": site,
            "waste": 0
        }

        fields={
            "url": True,
            "_id": False
        }

        try:
            urllist= (self.bdsearch.find(query, fields))
            if len(urllist) == 0:
                return None
            else:
                return urllist

        except:
            print('[Error] in query bdsearch url result from MongoDB')
            return None


    '''
    clockoff就是打卡下班的意思，当爬虫运行完时（如果能介入过程的话）
    应该调用此函数，把这次query到的url的'waste'字段都打为1，
    标记这个url已查询
    
    @ param {string} site   exm: 'news.qq.com'
    
    @ return {True|False}
    '''

    def clockoff(self, site):
        query = {
            "site": site,
            "waste": 0
        }

        try:
            return self.bdsearch.update_many(
                {"waste": 0},
                {"$set": {"waste": 1}}).acknowledged
        except:
            print('[Error] in change \'waste\' field in MongoDB')
            return False