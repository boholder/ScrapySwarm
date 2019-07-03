#!/usr/bin/python3
'''
@File : log_util.py

@Time : 2019/6/27

@Author : Boholder

@Function : 两个类，spider_log_util被爬虫调用，
            cc_log_util被swarm-api模块调用�
            向MongoDB的对应log集合中插入|更新内容�

            想了想，python logging 记录的信息太少了�
            只有一个等级一个信息，信息还整个是个str�
            干脆直接写个封装，再插入数据库�

            scrapy本身的log在swarm-api中控制是否写入一个文本文�
'''
import copy
import logging
import re

import scrapy

from ScrapySwarm.tools.time_format_util \
    import getUTCDateTimeObj

from ScrapySwarm.control.DBAccess import LogDBAccessUtil

'''

'''


class SpiderLogUtil(object):
    def __init__(self):
        self.logdb = LogDBAccessUtil()
        self.logger = logging.getLogger(__name__)

    def spider_start(self, spider=scrapy.Spider):
        self.logger.info('calling SpiderLogUtil.spider_start')
        logdict = {}

        logdict['spider'] = spider.name

        logdict['last_modified'] = \
            getUTCDateTimeObj()

        logdict['start_time'] = \
            spider.crawler.stats._stats['start_time']

        if self.logdb.addSpiderRunLog(logdict):
            self.logger.info('{0} start log successfully created'
                             .format(spider.name))

    def spider_finish(self, spider=scrapy.Spider):
        self.logger.info('calling SpiderLogUtil.spider_finish')
        logdict = {}
        statsdict = copy.deepcopy(spider.crawler.stats._stats)

        logdict['spider'] = spider.name

        logdict['last_modified'] = \
            getUTCDateTimeObj()

        logdict['start_time'] = \
            statsdict['start_time']
        if 'finish_time' in statsdict:
            logdict['finish_time'] = \
                statsdict['finish_time']

        if 'log_count/WARNING' in statsdict:
            logdict['log_count/WARNING'] = \
                statsdict['log_count/WARNING']
        if 'log_count/ERROR' in statsdict:
            logdict['log_count/ERROR'] = \
                statsdict['log_count/ERROR']

        if 'downloader/request_count' in statsdict:
            logdict['downloader/request_count'] = \
                statsdict['downloader/request_count']
        if 'downloader/response_count' in statsdict:
            logdict['downloader/response_count'] = \
                statsdict['downloader/response_count']
        if 'downloader/response_bytes' in statsdict:
            logdict['downloader/response_bytes'] = \
                statsdict['downloader/response_bytes']

        # response count diff via http response status code
        for key in statsdict.keys():
            if re.search('downloader/response_status_count/', key):
                logdict[key] = statsdict[key]

        if 'item_scraped_count' in statsdict:
            logdict['item_scraped_count'] = \
                statsdict['item_scraped_count']

        if 'finish_reason' in statsdict:
            logdict['finish_reason'] = \
                statsdict['finish_reason']

        if self.logdb.updateSpiderFinishStats(logdict):
            self.logger.info('{0} finish log successfully updated'
                             .format(spider.name))


class APILogUtil(object):
    def __init__(self):
        self.logdb = LogDBAccessUtil()
        self.logger = logging.getLogger(__name__)

    def api_start(self, loggingdict):
        self.logger.info('calling APILogUtil.api_start')
        logdict = {}

        logdict['api_name'] = loggingdict['api_name']

        logdict['last_modified'] = \
            getUTCDateTimeObj()

        logdict['start_time'] = loggingdict['start_time']

        if self.logdb.addAPICallingLog(logdict):
            self.logger.info('{0} start log successfully created'
                             .format(logdict['api_name']))

    def api_finish(self, loggingdict):
        self.logger.info('calling APILogUtil.api_finish')
        logdict = {}

        logdict['api_name'] = loggingdict['api_name']

        logdict['last_modified'] = \
            getUTCDateTimeObj()

        logdict['start_time'] = loggingdict['start_time']

        logdict['finish_time'] = loggingdict['finish_time']

        logdict['argsdict'] = loggingdict['argsdict']

        logdict['finish_reason'] = loggingdict['finish_reason']

        if self.logdb.updateAPIFinishLog(logdict):
            self.logger.info('{0} finish log successfully created'
                             .format(logdict['api_name']))
