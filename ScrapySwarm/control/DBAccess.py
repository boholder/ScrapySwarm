#!/usr/bin/python3
'''
@File : DBAccess.py

@Time : 2019/6/25

@Author : Boholder

@Function : 建立mongodb连接并执行数据库CURD操作。
            含以下几个类：
            1.UniqueDBInsertUtil,建立索引并设置主键，
            确保DB保存的数据不重复，在pipelines.py中被调用。

            2.BDsearchUrlUtil，
                getNewUrl()
                从MongoDB拉取，由百度爬虫爬下的目标网站的文章的url，
                生成列表并返回。
                clockoff()
                改写'waste'字段标明已使用过这次查到的url

                该模块被其他需要借助百度搜索提供url的爬虫们调用。

            3.NormalDBInsertUtil,普通的插入新数据，
                由pipeline调用

            4.LogDBAccessUtil,为centercontrol.log_util调用，
                插入或更新DB中的日志表

'''
import datetime
import os

import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy import cmdline

import ScrapySwarm.items as items

from ScrapySwarm.tools.imag import download_pic

from ScrapySwarm.settings import \
    LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, MONGO_DB_NAME, \
    COLL_BAIDU_SREACH, COLL_CHINA_NEWS, COLL_WEIBO_COMMENTS, \
    COLL_WEIBO_INFOMATION, COLL_WEIBO_RELATIONSHIPS, COLL_WEIBO_TWEETS, \
    COLL_QQ_NEWS, COLL_SINA_NEWS, \
    LOG_DB_NAME, COLL_SPIDERS_LOG, COLL_API_LOG

connection = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)


class UniqueDBInsertUtil(object):
    '''
    初始化，连接数据库之类
    '''

    def __init__(self):

        db = connection[MONGO_DB_NAME]
        self.Tweets = db[COLL_WEIBO_TWEETS]
        self.Comments = db[COLL_WEIBO_COMMENTS]
        self.Chinanews = db[COLL_CHINA_NEWS]
        self.QQNews = db[COLL_QQ_NEWS]
        self.SinaNews = db[COLL_SINA_NEWS]

        # create news collection unique index
        newsfield = [
            ("url", pymongo.DESCENDING),
            ("title", pymongo.ASCENDING)
        ]
        self.Chinanews.create_index(newsfield, unique=True)
        self.QQNews.create_index(newsfield, unique=True)
        self.SinaNews.create_index(newsfield, unique=True)

        # baidu search unique index
        self.BDSearch = db[COLL_BAIDU_SREACH]
        bdfield = [
            ("url", pymongo.ASCENDING)
        ]
        self.BDSearch.create_index(bdfield, unique=True)

        # 剩下的你对照着加吧，你那个weibo可能因为爬取类型不同，要写不只一个索引
        # 索引是对应单个集合的，
        # 所以实际上我上面那个没必要两个新闻统一一个索引

        # weibo collection unique index
        field = {
            "1": 1
        }

    '''
    
    '''

    def BDUniqueInsert(self, item):
        if isinstance(item, items.BaiduSearchItem):
            self.BDSearch.insert(dict(item))

    def newsUniqueInsert(self, item):
        try:
            if isinstance(item, items.ChinaNewsItem):
                self.Chinanews.insert(dict(item))
                # folderpath = "E:\chinanews" + item['keyword'];
                #
                # for img in item['imgs']:
                #     image_path1 = img.split("/")[-1]
                #     image_path1 = item["url"].split("/")[-1] + image_path1
                #     image_path = os.path.join(folderpath, image_path1)
                #     download_pic(img, image_path)
            elif isinstance(item, items.QQNewsItem):
                self.QQNews.insert(dict(item))
            elif isinstance(item, items.SinaNewsItem):
                self.SinaNews.insert(dict(item))

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            # (每次运行因为客观原因必然爬取到大量重复数据)
            pass

    def commentsUniqueInsert(self, item):
        try:
            self.Comments.insert(item)
            # if isinstance(item, items.CommentItem):
            #     last = self.Comments.find_one({'_id': item['_id']})
            #     if last:
            #         # last=last[0]
            #         print(last)
            #         if last['']:
            #             last['crawl_time'].append(item['crawl_time'][0])
            #             last['like_num'].append(item['like_num'][0])
            #             last['repost_num'].append(item['repost_num'][0])
            #             last['comment_num'].append(item['comment_num'][0])
            #             self.Tweets.update({"_id": last['_id']}, {"$set": last})
            #
            #
            #     else:
            #         self.Tweets.insert(dict(item))

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            pass

    def weiboUniqueInsert(self, item):
        try:
            if isinstance(item, items.TweetsItem):
                last = self.Tweets.find_one({'_id': item['_id']})
                if last:
                    # last=last[0]
                    print(last)
                    if len(last['crawl_time']) <= 3:
                        last['crawl_time'].append(item['crawl_time'][0])
                        last['like_num'].append(item['like_num'][0])
                        last['repost_num'].append(item['repost_num'][0])
                        last['comment_num'].append(item['comment_num'][0])
                        self.Tweets.update({"_id": last['_id']}, {"$set": last})


                else:
                    self.Tweets.insert(dict(item))

                    # folderpath = "e:\weibo" + item['keyword'];
                    # if 'image_url' in item:
                    #     print("保存")
                    #     image_path1 = item['image_url'].split("/")[-1]
                    #     image_path = os.path.join(folderpath, image_path1)
                    #     download_pic(item['image_url'], image_path)

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            pass

    def export(self,  keyword, source=None, aftertime=None):
        dic={"keyword":keyword}
        if aftertime:
            dic['crawl_time']={ "$gt": aftertime }
        last = self.Tweets.find(dic)
        return last




class NormalDBInsertUtil(object):
    def __init__(self):
        db = connection[MONGO_DB_NAME]
        self.Information = db[COLL_WEIBO_INFOMATION]
        self.Relationships = db[COLL_WEIBO_RELATIONSHIPS]

    def insert_item(self, item):
        try:
            if isinstance(item, items.RelationshipsItem):
                self.Relationships.insert(dict(item))
            else :
                self.Information.insert(dict(item))

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以
            pass


class BDsearchUrlUtil(object):
    '''
    初始化，连接数据库之类
    '''

    def __init__(self):

        db = connection[MONGO_DB_NAME]
        self.bdsearch = db[COLL_BAIDU_SREACH]

    '''
    从mongodb中按'site'表项读取所有“新的('waste'=0)”url,
    组成url列表并返回列表

    @ param {string} site   exm: 'news.qq.com'

    @ param {string} keyword exm: '中美贸易'

    @ return {List|None}  [url1,url2,url3,...] 
                            urlexm: 'http://baidu.com/...'
                          None for no new url
    '''

    def getNewUrl(self, site, keyword):
        # construct query and fliter
        query = {
            "site": site,
            "keyword": keyword,
            "waste": 0
        }

        fields = {
            "url": True,
            "_id": False
        }

        urllist = list(self.bdsearch.find(query, fields))
        if len(urllist) == 0:
            return None
        else:
            return [one['url'] for one in urllist]

    '''
    clockoff就是打卡下班的意思，当爬虫运行完时（如果能介入过程的话）
    应该调用此函数，把这次query到的url的'waste'字段都打为1，
    标记这个url已查询

    @ param {string} site   exm: 'news.qq.com'

    @ param {string} keyword exm: '中美贸易'

    @ return {True|False}
    '''

    def clockoff(self, site, keyword):
        query = {
            "site": site,
            "keyword": keyword,
            "waste": 0
        }

        return self.bdsearch.update_many(
            {"waste": 0},
            {"$set": {"waste": 1}}
        ).acknowledged


class LogDBAccessUtil(object):
    def __init__(self):
        db = connection[LOG_DB_NAME]
        self.Spiderslog = db[COLL_SPIDERS_LOG]
        self.APIlog = db[COLL_API_LOG]

    def addSpiderRunLog(self, logdict):
        return self.Spiderslog \
            .insert_one(logdict).acknowledged

    def updateSpiderFinishStats(self, logdict):
        return self.Spiderslog.update_one(
            {"spider": logdict['spider'],
             "start_time": {'$lt': datetime.datetime.now(),
                            '$gt': logdict['start_time']
                                   - datetime.timedelta(seconds=1)}},
            {"$set": logdict}
        ).acknowledged

    def addAPICallingLog(self, logdict):
        return self.APIlog \
            .insert_one(logdict).acknowledged

    def updateAPIFinishLog(self, logdict):
        return self.APIlog.update_one(
            {"api_name": logdict['api_name'],
             "start_time": {'$lt': datetime.datetime.now(),
                            '$gt': logdict['start_time']
                                   - datetime.timedelta(seconds=1)}},
            {"$set": logdict}
        ).acknowledged
