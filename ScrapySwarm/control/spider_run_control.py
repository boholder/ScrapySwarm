#!/usr/bin/python3
'''
@File : spider_run_control.py

@Time : 2019/7/1

@Author : Boholder

@Function : run spiders using python script.
            https://docs.scrapy.org/en/latest/topics/practices.html#

'''
import os
from multiprocessing import Pool

from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
import logging
import time

from ScrapySwarm.tools.time_format_util \
    import getCurrentTimeReadable

from ScrapySwarm.spiders import qqnews_spider


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

        # if log and not settings:
        #     logfilename = getCurrentTimeReadable() \
        #                   + '-' + spidername + '.log'
        #     settings = {
        #         "LOG_FILE": logfilename
        #     }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        configure_logging(settings)

        runner = CrawlerRunner(get_project_settings())
        yield runner.crawl('baidusearch', q=keyword, site=site)
        yield runner.crawl(spidername, q=keyword)
        reactor.stop()

    def run(self, spidername, keyword, log=True, settings=None):
        self.logger.info('Spider baidusearch begin to run...')
        start = time.time()

        self.crawl(spidername, keyword, log, settings)
        reactor.run()

        # middle = time.time()
        # self.logger.info(
        #     'Spider baidusearch finished, time used: {0} seconds.'
        #         .format((middle - start)))
        # self.logger.info('Spider \"{0}\" begin to run...'
        #                  .format(spidername))

        end = time.time()
        self.logger.info(
            'Spider \"{0}\" finished, time used: {1} seconds.'
                .format(spidername, (end - start)))


class DirectUrlSpiderProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def crawl(self, spidername, keyword, log=True, settings=None):

        # if log and not settings:
        #     logfilename = getCurrentTimeReadable() \
        #                   + '-' + spidername + '.log'
        #     settings = {
        #         "LOG_FILE": logfilename
        #     }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        # process = CrawlerProcess(get_project_settings())

        runner = CrawlerRunner(get_project_settings())

        d = runner.crawl(spidername, q=keyword)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def run(self, spidername, keyword, log=True, settings=None):
        self.logger.info('Spider \"{0}\" begin to run...'
                         .format(spidername))
        start = time.time()

        self.crawl(spidername, keyword, log, settings)

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

        def prog(spidername, keyword, log=True, settings=None):
            if spidername == 'qqnews' \
                    or spidername == 'sinanews':
                processor = BDAssistSpiderProcessor()
            else:
                processor = DirectUrlSpiderProcessor()

            processor.run(spidername, keyword, log, settings)

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
                                 (spidername, keyword,
                                  log, settings))

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
            for config in runconfiglist:
                spidername = config['spidername']
                keyword = config['keyword']

                log = True
                if 'log' in config:
                    log = config['log']

                settings = None
                if 'settings' in config:
                    settings = config['settings']

                # it will block every time until return back
                prog(spidername, keyword, log, settings)

    # This function only generate one log file
    # All spiders share one settings.
    #
    # And note that this method can ONLY active
    #   direct url spiders like chinanews_spider.

    def runSameSettings(self, spiders,
                        keyword, log=True, settings=None):

        # if log and not settings:
        #     logfilename = getCurrentTimeReadable() \
        #                   + '-run-all.log'
        #     settings = {
        #         "LOG_FILE": logfilename
        #     }

        # https://docs.scrapy.org/en/latest/topics
        # /api.html#scrapy.settings.Settings
        configure_logging(settings)

        process = CrawlerProcess()
        for spider in spiders:
            process.crawl(spider, q=keyword)

        d = process.join()
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
        # 不能一起运行，因为我有些爬虫需要百度先爬。
        # 但我给你写了个 runSameSettings() 函数，
        # 如果你想用的话

        # spiders = ['qqnews', 'sinanews']

        spiders =['chinanews_spider']

        runconfiglist=[]

        for spider in spiders:
            config={
                "spidername": spider,
                "keyword": keyword
            }
            runconfiglist.append(config)

        self.runINDEPSettings(runconfiglist)
