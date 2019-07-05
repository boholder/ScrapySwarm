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
import copy
import datetime

import pymongo
from pymongo.errors import DuplicateKeyError

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
    def __init__(self, keyword):
        self.dict = {
            "keyword": keyword,
            "last_modified": datetime.datetime.utcnow(),
            "item_num_dict": {},
            "old_item_num_dict": {}
        }

    def get_dict(self):
        return self.dict


class CounterDBAccess(object):
    def __init__(self):
        connection = \
            pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)

        dblog = connection[DB_LOG_NAME]

        self.stats_coll = dblog[COLL_STATISTICS_NAME]

        # create unique index
        field = [("keyword", pymongo.ASCENDING)]
        self.stats_coll.create_index(field, unique=True)

        self.dbdata = connection[DB_DATA_NAME]

        self.counter_item_dict = {}

        self.new_counter_item_dict = {}

    def get_all_keywords(self, pre_counter_items_dict):

        # inheriting results from the previous loop
        # to judge old | new keyword,
        # to decide insert | update in statistics collection
        self.counter_item_dict = copy.deepcopy(pre_counter_items_dict)

        # query every collection for all keywords exist
        for coll_data_name in COLL_DATA_NAME_LIST:

            coll = self.dbdata[coll_data_name]

            # add new keyword into keyword_list
            for keyword in coll.find().distinct('keyword'):
                if keyword not in self.counter_item_dict.keys():
                    self.new_counter_item_dict[keyword] = None

    def query_and_counter(self):

        # query every collection about that keyword
        def query(keyword, item=CounterItem):
            for coll_data_name in COLL_DATA_NAME_LIST:
                coll = self.dbdata[coll_data_name]
                filter = {"keyword": keyword}

                # update|create key-value pair in item_num_dict
                # key: data collection's name
                # value: number of items that have this keyword
                item.get_dict()['item_num_dict'][coll_data_name] = \
                    coll.count_documents(filter)

        # update old counter items' dict value
        for keyword in self.counter_item_dict.keys():
            self.counter_item_dict[keyword].dict['old_item_num_dict'] = \
                self.counter_item_dict[keyword].dict['item_num_dict']
            self.counter_item_dict[keyword].dict['last_modified'] = \
                datetime.datetime.utcnow()

        # create new counter items for new keyword
        for keyword in self.new_counter_item_dict.keys():
            self.new_counter_item_dict[keyword] = CounterItem(keyword)

        # add two dict into one
        self.counter_item_dict.update(self.new_counter_item_dict)

        # query DB & update every counter item's value
        for keyword in self.counter_item_dict.keys():
            query(keyword, self.counter_item_dict[keyword])

        return copy.deepcopy(self.counter_item_dict)

    def update_statistics(self):

        def update_old(itemdict):
            # avoid update '_id'
            self.stats_coll.find_one_and_update(
                {"keyword": itemdict['keyword']},
                {"$set": {"last_modified": itemdict['last_modified'],
                          "item_num_dict": itemdict['item_num_dict'],
                          "old_item_num_dict": itemdict['old_item_num_dict']}}
            )

        # If this module isn't running since DB initial,
        #   there may be 'old' keyword items already in DB.
        # While this module first see them
        #   and considers them as 'new' keywords.
        # Try to insert such one will throw a DuplicateKeyError
        for item in self.counter_item_dict.values():
            try:
                self.stats_coll.insert_one(item.get_dict())
            except DuplicateKeyError:
                update_old(item.get_dict())


if __name__ == '__main__':
    counter_item_dict = {}
    while True:
        dba = CounterDBAccess()
        dba.get_all_keywords(counter_item_dict)
        counter_item_dict = dba.query_and_counter()
        dba.update_statistics()