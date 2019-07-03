# -*- coding: utf-8 -*-

# Scrapy settings for ScrapySwarm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ScrapySwarm'
COMMANDS_MODULE = 'ScrapySwarm.control'
SPIDER_MODULES = ['ScrapySwarm.spiders']
NEWSPIDER_MODULE = 'ScrapySwarm.spiders'

# MongoDB setting
LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017

# data db & collections name
MONGO_DB_NAME = 'WebData'
COLL_BAIDU_SREACH = 'baidu_search_results'
COLL_WEIBO_INFOMATION = 'weibo_infomation'
COLL_WEIBO_TWEETS = 'weibo_tweets'
COLL_WEIBO_COMMENTS = 'weibo_comments'
COLL_WEIBO_RELATIONSHIPS = 'weibo_relationships'
COLL_CHINA_NEWS = 'news_china'
COLL_QQ_NEWS = 'news_qq'
COLL_SINA_NEWS = 'news_sina'

# log db & collections name
LOG_DB_NAME = 'SwarmLog'
COLL_SPIDERS_LOG = 'spiders_log'
COLL_API_LOG = 'api_log'

# log file directory
LOG_DIR = './log/'

ITEM_PIPELINES = {'ScrapySwarm.pipelines.ScrapyswarmPipeline': 300, }
ROBOTSTXT_OBEY = False
