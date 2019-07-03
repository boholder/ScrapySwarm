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
from multiprocessing import Pool

from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import logging
import time

from ScrapySwarm.tools.time_format_util \
    import getCurrentTimeReadable

from ScrapySwarm.settings import LOG_DIR

from ScrapySwarm.tools.spider_exist_util import *


class BDAssistSpiderProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logfilename = ''

    @defer.inlineCallbacks
    def crawl(self, spidername, keyword,
              runner):

        site = ''
        if spidername == 'qqnews_spider':
            site = 'news.qq.com'
        elif spidername == 'sinanews_spider':
            site = 'news.sina.com.cn'

        therunner = runner

        yield therunner.crawl('baidu_search_spider', q=keyword, site=site)
        yield therunner.crawl(spidername, q=keyword)

    def run(self, spidername, keyword,
            log=True, runner=None, settings=None):

        if settings:
            thesettings = settings
        else:
            thesettings = copy.deepcopy(get_project_settings())

        if log and not settings:
            self.logfilename = LOG_DIR + getCurrentTimeReadable() \
                               + '-' + spidername + '.log'
            logfilename = self.logfilename
            thesettings['LOG_FILE'] = logfilename

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings

        configure_logging(thesettings)

        if runner:
            self.crawl(spidername, keyword,
                       runner)
        else:
            runner = CrawlerRunner(thesettings)

            self.logger.info('Spider baidusearch begin to run...')
            start = time.time()

            self.crawl(spidername, keyword,
                       runner)

            d = runner.join()
            d.addBoth(lambda _: reactor.stop())

            # it will block until return back
            reactor.run()

            end = time.time()
            self.logger.info(
                'Spider \"{0}\" finished, time used: {1} seconds.'
                    .format(spidername, (end - start)))

            if self.logfilename != '':
                return self.logfilename
            else:
                return True


class DirectUrlSpiderProcessor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logfilename = ''
        self.loop = 0

    def crawl(self, spidername, keyword,
              log=True, runner=None, settings=None):

        thesettings = copy.deepcopy(get_project_settings())

        if log and not settings:
            self.logfilename = LOG_DIR + getCurrentTimeReadable() \
                               + '-' + spidername + '.log'
            logfilename = self.logfilename
            thesettings['LOG_FILE'] = logfilename
        else:
            thesettings = settings

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        # process = CrawlerProcess(get_project_settings())

        if not runner:
            configure_logging(thesettings)
            therunner = CrawlerRunner(thesettings)
        else:
            therunner = runner

        d = therunner.crawl(spidername, q=keyword)

        if not runner:
            d.addBoth(lambda _: reactor.stop())



    def run(self, spidername, keyword, log=True, runner=None, settings=None):
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

            if self.logfilename != '':
                return self.logfilename
            else:
                return True

class WeiboSpiderProcessor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logfilename = ''
        self.loop = 0

    def crawl(self, spidername, keyword, times,
              log=True, runner=None, settings=None):

        thesettings = copy.deepcopy(get_project_settings())

        if log and not settings:
            self.logfilename = LOG_DIR + getCurrentTimeReadable() \
                               + '-' + spidername + '.log'
            logfilename = self.logfilename
            thesettings['LOG_FILE'] = logfilename
        else:
            thesettings = settings

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        # process = CrawlerProcess(get_project_settings())

        if not runner:
            configure_logging(thesettings)
            therunner = CrawlerRunner(thesettings)
        else:
            therunner = runner

        d = therunner.crawl(spidername, q=keyword, t = times)

        if not runner:
            d.addBoth(lambda _: reactor.stop())

        if  self.loop < 3:
            self.loop = self.loop + 1
            d.addBoth(lambda _: self.crawl(spidername, keyword, self.loop, log, runner, settings))

    def run(self, spidername, keyword, log=True, runner=None, settings=None):
        self.loop = 0
        self.crawl(spidername, keyword,self.loop, log, runner, settings)

        if not runner:
            self.logger.info('Spider \"{0}\" begin to run...'
                             .format(spidername))
            start = time.time()

            reactor.run()

            end = time.time()
            self.logger.info(
                'Spider \"{0}\" finished, time used: {1} seconds.'
                    .format(spidername, (end - start)))

            if self.logfilename != '':
                return self.logfilename
            else:
                return True

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
            if isBDAType(spidername):
                processor = BDAssistSpiderProcessor()
            elif spidername=="weibo_spider":
                processor = WeiboSpiderProcessor()
            else:
                processor =DirectUrlSpiderProcessor()

            processor.run(spidername, keyword, log, runner, settings)

        # # linux, use multiprocess
        # if os.name == 'posix':
        #     pool = Pool()
        #
        #     for config in runconfiglist:
        #         spidername = config['spidername']
        #         keyword = config['keyword']
        #
        #         log = True
        #         if 'log' in config:
        #             log = config['log']
        #
        #         settings = None
        #         if 'settings' in config:
        #             settings = config['settings']
        #
        #         pool.apply_async(prog,
        #                          (spidername, keyword, log,
        #                           None, settings))
        #
        #     self.logger.info('Multiprocess begin...')
        #     start = time.process_time()
        #     pool.close()
        #     pool.join()
        #     end = time.process_time()
        #     self.logger.info(
        #         'Multiprocess finished, time used: {0} seconds.'
        #             .format(end - start))

        # windows
        # elif os.name == 'nt':

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
        spiders =BDA_SPIDERS + ['chinanews_spider',"weibo_spider"]


        runconfiglist = []

        for spider in spiders:
            config = {
                "spidername": spider,
                "keyword": keyword
            }
            runconfiglist.append(config)

        self.runINDEPSettings(runconfiglist)