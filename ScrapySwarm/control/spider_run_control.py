#!/usr/bin/python3
'''
@File : spider_run_control.py

@Time : 2019/7/1

@Author : Boholder

@Function : run spiders using python script.
            https://docs.scrapy.org/en/latest/topics/practices.html#

'''
import copy
import os
from functools import wraps
from multiprocessing import Pool, Process
from queue import Queue

from scrapy import crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner

from scrapy.utils.log import configure_logging
import logging
import time

from ScrapySwarm.spiders.weibo_spider import WeiboSpider
from ScrapySwarm.tools.time_format_util \
    import getCurrentTimeReadable

from ScrapySwarm.settings import LOG_DIR


# from multiprocessing import Process, Queue


class BDAssistSpiderProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @defer.inlineCallbacks
    def crawl(self, spidername, keyword,
              log=True, runner=None, settings=None):

        site = ''
        if spidername == 'qqnews':
            site = 'news.qq.com'
        elif spidername == 'sinanews':
            site = 'news.sina.com.cn'

        if log and not settings:
            thesettings = copy.deepcopy(get_project_settings())
            logfilename = LOG_DIR + getCurrentTimeReadable() \
                          + '-' + spidername + '.log'
            thesettings['LOG_FILE']: logfilename
        else:
            thesettings = settings

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings

        if not runner:
            therunner = CrawlerRunner(thesettings)
        else:
            therunner = runner

        yield therunner.crawl('baidusearch', q=keyword, site=site)
        yield therunner.crawl(spidername, q=keyword)

        if not runner:
            reactor.stop()

    def run(self, spidername, keyword,
            log=True, runner=None, settings=None):

        self.crawl(spidername, keyword,
                   log, runner, settings)

        if not runner:
            self.logger.info('Spider baidusearch begin to run...')
            start = time.time()

            reactor.run()

            end = time.time()
            self.logger.info(
                'Spider \"{0}\" finished, time used: {1} seconds.'
                    .format(spidername, (end - start)))


class DirectUrlSpiderProcessor(object):
    loop = 0

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def crawl(self, spidername, keyword, log=True, runner=None, settings=None):
        print("当前是" + spidername)
        if log and not settings:
            thesettings = copy.deepcopy(get_project_settings())
            logfilename = LOG_DIR + getCurrentTimeReadable() \
                          + '-' + spidername + '.log'
            thesettings['LOG_FILE']: logfilename
        else:
            thesettings = settings

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        # process = CrawlerProcess(get_project_settings())

        if not runner:
            therunner = CrawlerRunner(thesettings)
        else:
            therunner = runner

        d = therunner.crawl(spidername, q=keyword)

        if not runner:
            d.addBoth(lambda _: reactor.stop())
        if spidername == "weibo_spider" and self.loop < 3:
            d.addBoth(lambda _: self.crawl(spidername, keyword, log, runner, settings))
            self.loop = self.loop + 1

    def run(self, spidername, keyword, log=True, runner=None, settings=None):
        self.loop = 0
        self.crawl(spidername, keyword, log, runner, settings)

        if not runner:
            self.logger.info('Spider \"{0}\" begin to run...'
                             .format(spidername))
            start = time.time()

            reactor.run()

            end = time.time()
            self.logger.info(
                'Spider \"{0}\" finished, time used: {1} seconds.'
                    .format(spidername, (end - start)))


class MultiSpidersProcessor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def runINDEPSettings(self, runconfiglist):
        # runconfiglist: [config1,config2,...]
        #
        # config: dict {spidername='',keyword='',
        #               log=True|False, settings=settings}
        #
        # https://docs.scrapy.org/en/latest/topics/
        # settings.html#topics-settings-ref

        def prog(spidername, keyword, log=True, runner=None, settings=None):
            if spidername == 'qqnews' \
                    or spidername == 'sinanews':
                processor = BDAssistSpiderProcessor()
            else:
                processor = DirectUrlSpiderProcessor()

            processor.run(spidername, keyword, log, runner, settings)

        # linux, use multiprocess
        if os.name == 'posix':
            pool = Pool()

            for config in runconfiglist:
                spidername = config['spidername']
                keyword = config['keyword']

                log = True
                if 'log' in config:
                    log = config['log']

                settings = None
                if 'settings' in config:
                    settings = config['settings']

                pool.apply_async(prog,
                                 (spidername, keyword, log,
                                  None, settings))

            self.logger.info('Multiprocess begin...')
            start = time.process_time()
            pool.close()
            pool.join()
            end = time.process_time()
            self.logger.info(
                'Multiprocess finished, time used: {0} seconds.'
                    .format(end - start))

        # windows
        elif os.name == 'nt':

            settings = copy.deepcopy(get_project_settings())
            logfile = LOG_DIR + \
                      getCurrentTimeReadable() + '-all-spider.log'
            settings['LOG_FILE'] = logfile
            configure_logging(settings)

            runner = CrawlerRunner(settings)

            for config in runconfiglist:
                spidername = config['spidername']
                keyword = config['keyword']

                log = True
                if 'log' in config:
                    log = config['log']

                settings = None
                if 'settings' in config:
                    settings = config['settings']

                prog(spidername, keyword, log, runner, settings)

            d = runner.join()
            d.addBoth(lambda _: reactor.stop())

            # it will block every time until return back
            reactor.run()

        # This function only generate one log file
        # All spiders share one settings.
        #
        # And note that this method can ONLY active
        #   direct url spiders like chinanews_spider.

        # !!!it has error!!!

    def runSameSettings(self, spiders,
                        keyword, log=True, settings=None):
        if log and not settings:
            logfilename = LOG_DIR + getCurrentTimeReadable() \
                          + '-spiders-all.log'
            settings = {
                "LOG_FILE": logfilename
            }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        configure_logging(settings)

        runner = CrawlerRunner(settings)
        for spider in spiders:
            runner.crawl(spider, q=keyword)

        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        self.logger.info('All spiders \"{0}\" begin to run...')
        start = time.time()

        # the script will block here
        # until all crawling jobs are finished
        reactor.run()

        end = time.time()
        self.logger.info(
            'All spiders\' job finished, time used: {0} seconds.'
                .format((end - start)))

    def runAll(self, keyword):
        self.loop = 0
        spiders = [
            'qqnews', 'sinanews', "chinanews_spider", "weibo_spider"]

        runconfiglist = []

        for spider in spiders:
            config = {
                "spidername": spider,
                "keyword": keyword
            }
            runconfiglist.append(config)

        self.runINDEPSettings(runconfiglist)
