#!/usr/bin/python3
'''
@File : spider_run_control.py

@Time : 2019/7/1

@Author : Boholder

@Function : run spiders using python script.
            https://docs.scrapy.org/en/latest/topics/practices.html#

'''

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import logging
import time

from ScrapySwarm.tools.time_format_util \
    import getCurrentTimeReadable


class BDAssistSpiderProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @defer.inlineCallbacks
    def crawl(self, spidername, keyword, log=True, settings=None):
        site = ''
        if spidername == 'qqnews':
            site = 'news.qq.com'
        elif spidername == 'sinanews':
            site = 'news.sina.com.cn'

        if log and not settings:
            logfilename = getCurrentTimeReadable() \
                          + '-' + spidername + '.log'
            settings = {
                "LOG_FILE": logfilename
            }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        configure_logging(settings)

        runner = CrawlerRunner()
        yield runner.crawl('baidusearch', q=keyword, site=site)
        yield runner.crawl(spidername, q=keyword)
        reactor.stop()

    def run(self, spidername, keyword, log=True, settings=None):
        self.logger.info('Spider \"{0}\" begin to run...'
                         .format(spidername))
        start = time.time()

        self.crawl(spidername, keyword, log, settings)
        reactor.run()

        end = time.time()
        self.logger.info(
            'Spider \"{0}\" finished, time used: {1} seconds.'
                .format(spidername, (end - start)))


class DirectUrlSpiderProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def crawl(self, spidername, keyword, log=True, settings=None):
        if log and not settings:
            logfilename = getCurrentTimeReadable() \
                          + '-' + spidername + '.log'
            settings = {
                "LOG_FILE": logfilename
            }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        configure_logging(settings)

        runner = CrawlerRunner()
        d = runner.crawl(spidername, q=keyword)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def run(self, spidername, keyword, log=True, settings=None):
        self.logger.info('Spider \"{0}\" begin to run...'
                         .format(spidername))
        start = time.time()

        self.crawl(spidername, keyword, log, settings)
        reactor.run()

        end = time.time()
        self.logger.info(
            'Spider \"{0}\" finished, time used: {1} seconds.'
                .format(spidername, (end - start)))
