#!/usr/bin/python3
'''
@File : unique_db_insert_util.py

@Time : 2019/6/25

@Author : Boholder

@Function : 

'''
import os

import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy import cmdline

import ScrapySwarm.items as items
from ScrapySwarm.tools.imag import download_pic


class UniqueDBInsertUtil(object):
    '''
    初始化，连接数据库之类
    '''

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
        self.Chinanews = db[COLL_CHINA_NEWS]
        self.QQNews = db[COLL_QQ_NEWS]
        self.SinaNews = db[COLL_SINA_NEWS]

        # create news collection unique index
        field = [
            ("url", pymongo.DESCENDING),
            ("time", pymongo.ASCENDING)
        ]
        self.Chinanews.create_index(field, unique=True)
        self.QQNews.create_index(field, unique=True)
        self.SinaNews.create_index(field, unique=True)

        # 剩下的你对照着加吧，你那个weibo可能因为爬取类型不同，要写不只一个索引
        # 索引是对应单个集合的，
        # 所以实际上我上面那个没必要两个新闻统一一个索引

        # weibo collection unique index
        field = {
            "1": 1
        }

    '''
    
    '''

    def newsUniqueInsert(self, item):
        try:
            if isinstance(item, items.ChinaNewsItem):
                self.Chinanews.insert(dict(item))
                folderpath = "E:\chinanews" + item['keyword'];

                for img in item['imgs']:
                    image_path1 = img.split("/")[-1]
                    image_path1 = item["url"].split("/")[-1] + image_path1
                    image_path = os.path.join(folderpath, image_path1)
                    download_pic(img, image_path)
            elif isinstance(item, items.QQNewsItem):
                self.QQNews.insert(dict(item))
            elif isinstance(item, items.SinaNewsItem):
                self.SinaNews.insert(dict(item))

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            pass

    def commentsUniqueInsert(self, item):
        try:
            if True:
                folderpath = "e:\weibo"

                image_path1 = item['comment_user_id'].split("/")[-1]+'.jpg'
                image_path = os.path.join(folderpath, image_path1)
                download_pic(item['head_url'], image_path)
                self.Comments.insert(item)

        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            pass


    def weiboUniqueInsert(self,item):
        try:
            if isinstance(item, items.TweetsItem):
                last = self.Tweets.find_one({'_id': item['_id']})
                if last:
                    # last=last[0]
                    print(last)
                    if len(last['crawl_time'])<=3:
                        last['crawl_time'].append(item['crawl_time'][0])
                        last['like_num'].append(item['like_num'][0])
                        last['repost_num'].append(item['repost_num'][0])
                        last['comment_num'].append(item['comment_num'][0])
                        self.Tweets.update({"_id":last['_id']},{"$set":last})


                else:
                    self.Tweets.insert(dict(item))
                    print("保存空的了")
                    folderpath = "e:\weibo" + item['keyword'];
                    if 'image_url' in item:
                        print("保存")
                        image_path1 = item['image_url'].split("/")[-1]
                        image_path = os.path.join(folderpath, image_path1)
                        download_pic(item['image_url'], image_path)



        except DuplicateKeyError:
            # 有重复数�
            # 不做处理也可以，结果是没插入成功，
            # 就是不让raise error了
            pass