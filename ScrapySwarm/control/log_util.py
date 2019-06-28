#!/usr/bin/python3
'''
@File : log_util.py

@Time : 2019/6/27

@Author : Boholder

@Function : 两个类，spider_log_util被爬虫调用，
            cc_log_util被cc-api模块调用，
            向MongoDB的对应log集合中插入|更新内容。

            想了想，python logging 记录的信息太少了，
            只有一个等级一个信息，信息还整个是个str。
            干脆直接写个封装，再插入数据库。

            scrapy本身的log在cc-api中控制是否写入一个文本文件
'''

import logging
import scrapy

from ScrapySwarm.tools.time_format_util \
    import getCurrentTime, getCurrentTimeReadable,\
            getUTCDateTimeObj

from ScrapySwarm.tools.DBAccess import LogDBAccessUtil


'''

'''


class spider_log_util(object):
    def __init__(self):
        self.logdb = LogDBAccessUtil()

    def spider_start(self, spider=scrapy.Spider):
        logdict = {}

        logdict['spider'] = spider.name

        logdict['start_time'] = getCurrentTime()
        logdict['start_time_readable'] = getCurrentTimeReadable()
        logdict['last_modified_utc']=getUTCDateTimeObj()

        print(spider.stats)

        if self.logdb.addSpiderRunLog(logdict):
            logging.info('{0} start log successfully created'
                         .format(spider.name))

    def spider_close(self, spider=scrapy.Spider):
        logdict={}

        logdict['spider']=spider.name

        logdict['close_time'] = getCurrentTime()
        logdict['close_time_readable'] = getCurrentTimeReadable()
        logdict['last_modified_utc'] = getUTCDateTimeObj()

        if self.logdb.addSpiderRunLog(logdict):
            logging.info('{0} close log successfully updated'
                         .format(spider.name))


class api_log_util(object):
    def __init__(self):
        logdb = LogDBAccessUtil()
