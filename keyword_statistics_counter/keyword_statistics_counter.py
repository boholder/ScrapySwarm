#!/usr/bin/python3
'''
@File : keyword_statistics_counter.py

@Time : 2019/7/4

@Author : Boholder

@Function : Assist module which should be run through console
            WHENEVER the ScrapySwarm project is running (the spiders).

            * What it do:

            It runs a infinite loop,
            count items (by keyword) number crawled by spiders,
            by querying from MongoDB using pymongo module,
            and then maintain a statistics collection in MongoDB
            by updating each keyword's crawled number record.

            * What it for:

            It serves the corresponding
            'spiders running status display controler'
            in the web server back-end.

            Yeh this module and one controler in back-end
            share data via statistics collection.
            Importantly, this process is real-time,
            since I found asynchronous python isn't so easy to code.

            * Statistics collection structure:

                |_id    (Mongodb auto-generating)
                |{str}  keyword
                |{datetime obj (UTC)} last_modified
                |{dict} item_num_dict
                    {"site1 domain":{int}   crawled number,
                     "site2 domain":{int}   crawled number,
                     ...
                     }
                |{dict} old_item_num_dict
                    the value of item_num_dict before last update
'''
import datetime

import pymongo

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_LOG_NAME = 'SwarmLog'
DB_DATA_NAME = 'WebData'

COLL_STATISTICS_NAME = 'keyword_statistics'

# (In MongoDB) item collections' name list
COLL_DATA_NAME_LIST = ['news_china', 'news_sina', 'news_qq',
                       'weibo_comment', 'weibo_infomation',
                       'weibo_tweets']


class CounterItem(object):
    dict = {
        "keyword": None,
        "last_modified": None,
        "item_num_dict": {},
        "old_item_num_dict": {}
    }

    def __init__(self, keyword):
        self.dict['keyword'] = keyword
        self.dict['last_modified'] = datetime.datetime.utcnow()


class CounterDBAccess(object):
    def __init__(self):
        connection = \
            pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)

        dblog = connection[DB_LOG_NAME]

        self.stats_coll = dblog[COLL_STATISTICS_NAME]

        # create unique index
        newsfield = [
            ("keyword", pymongo.ASCENDING)
        ]
        self.stats_coll.create_index(newsfield, unique=True)

        self.dbdata = connection[DB_DATA_NAME]

        self.counter_item_dict = {}

        self.new_couter_item_dict = {}

    def query_and_counter(self):

        def query(keyword, item=CounterItem):
            # query every collection about that keyword
            for coll_data_name in COLL_DATA_NAME_LIST:
                coll = self.dbdata[coll_data_name]
                ##################################
                ################################
                ###################################33
                #################################

        for keyword in self.counter_item_dict.keys():
            query(keyword, self.counter_item_dict[keyword])

        for keyword in self.new_couter_item_dict.keys():
            self.new_couter_item_dict[keyword] = CounterItem(keyword)
            query(keyword, self.new_counter_item_dict[keyword])

    def update_statistics(self):

        for item in self.counter_item_dict.values():
            self.stats_coll.update_one(
                {"keyword": item.dict['keyword']},
                {"$set": item.dict}
            )

        for item in self.new_couter_item_dict.values():
            self.stats_coll.insert_one(item.dict)

    def get_all_keywords(self, pre_counter_item_dict):

        # inheriting results from the previous loop
        # to judge old | new keyword,
        # to decide insert | update in statistics collection
        self.counter_item_dict = pre_counter_item_dict

        # query every collection for all keywords exist
        for coll_data_name in COLL_DATA_NAME_LIST:

            coll = self.dbdata[coll_data_name]

            # add new keyword into keyword_list
            for keyword in coll.find().distinct('keyword'):
                if keyword not in self.counter_item_dict.keys():
                    self.new_couter_item_dict[keyword] = None
