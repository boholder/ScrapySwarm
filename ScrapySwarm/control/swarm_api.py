#!/usr/bin/python3
'''
@File : swarm_api.py

@Time : 2019/7/1

@Author : Boholder

@Function : API for upper system to
            run spider, read swarm's log etc.

'''

import logging
import threading

from ScrapySwarm.control.spider_run_control \
    import OneSpiderProcessor, MultiSpidersProcessor
from ScrapySwarm.tools.spider_exist_util import exist
from ScrapySwarm.control.log_util import APILogUtil
from ScrapySwarm.tools.time_format_util import getUTCDateTimeObj

apilogutil = APILogUtil()

logger = logging.getLogger(__name__)

'''
Run one spider in project, get process's log in return

@ param {str} spidername: spider class 'name' variable

@ param {str} keyword: keyword for search in the site

@ param {bool} log: True(default), output log into a file
                    False, log settings obey 'settings' param
                    see 
    https://docs.scrapy.org/en/latest/topics/settings.html#log-file
                    for more

@ param {dict} settings: same as above (None default)

@ param {int} repeatnum: Make the spider run several times in a chain
                            (None default)

@ return {bool} if no log file generated, return process result
         {list} log text, one index per line 
                    (already remove '\n' behind every line)
         {None} something throw error inside file I/O code

'''


def runOneSpider(spidername, keyword,
                 log=True, settings=None, repeatnum=None):
    def prog(spidername, keyword, log, settings, repeatnum):
        # prepare to log api's begin
        argsdict = {
            "spidername": spidername,
            "keyword": keyword,
            "log": log,
            "settings": settings
        }

        logdict = {
            "api_name": runOneSpider.__name__,
            "start_time": getUTCDateTimeObj(),
            "argsdict": argsdict
        }

        logger.info('calling ' + runOneSpider.__name__)
        apilogutil.api_start(logdict)

        # judge spidername exist in project or not
        # Spider.name MUST equal to python file name
        # due to implement method
        if not exist(spidername):
            logdict['finish_time'] = getUTCDateTimeObj()

            logdict['finish_reason'] = \
                'given spider name not found under \'spider\' dir' \
                '(it may because spider\'s name var ' \
                'not equal to class file\'s name)'

            apilogutil.api_finish(logdict)

            logger.info(runOneSpider.__name__ + ' finished.')

            return False

        # run it, stuck until get return

        processor = OneSpiderProcessor()
        logfilename = processor.run(spidername, keyword,
                                    log, None,
                                    settings, repeatnum)

        logdict['finish_time'] = getUTCDateTimeObj()

        # return this process's log (by reading log file)
        # or return a bool
        if type(logfilename) == str:
            try:
                with open(logfilename, 'r', encoding='utf-8') as f:
                    pass
                #     loglist = f.readlines()
                #     loglist = [line.strip() for line in loglist]
                #
                # logdict['finish_reason'] = 'api finished normally.'
                # apilogutil.api_finish(logdict)
                # logger.info(runOneSpider.__name__ + ' finished.')
                # return loglist
            except IOError:
                logdict['finish_reason'] = \
                    runOneSpider.__name__ + \
                    ' run finished, ' \
                    'but can\' t open expect log file' \
                    '(I/O error threw).'
                apilogutil.api_finish(logdict)
                logger.info(runOneSpider.__name__ +
                            ' finished with I/O error.')
                return None

        else:
            logdict['finish_reason'] = 'api finished without a logfile'
            apilogutil.api_finish(logdict)
            return True

    t = threading.Thread(target=prog,
                         args=(spidername, keyword,
                               log, settings, repeatnum))
    t.daemon = True
    t.start()


'''
Just run all spiders that can be ran.

@ param {str} keyword: only need it to config spider

@ return {None}
'''


def runAllSpider(keyword):
    def prog(keyword):
        argsdict = {
            "keyword": keyword
        }

        logdict = {
            "api_name": runAllSpider.__name__,
            "start_time": getUTCDateTimeObj(),
            "argsdict": argsdict
        }

        logger.info('calling ' + runAllSpider.__name__)
        apilogutil.api_start(logdict)

        m = MultiSpidersProcessor()
        m.runAll(keyword)

        logdict['finish_time'] = getUTCDateTimeObj()
        logdict['finish_reason'] = 'api finished normally'

        apilogutil.api_finish(logdict)
        logger.info(runAllSpider.__name__ + ' finished.')

    t = threading.Thread(target=prog,
                         args=(keyword,))
    t.daemon = True
    t.start()
    return t


'''
Run more than one spiders with each one given different settings

@ param {list} runconfiglist: [config1,config2,...]
        #
        # config: dict {spidername='',keyword='',
        #               log=True|False, settings=settings}
        #
        # https://docs.scrapy.org/en/latest/topics/
        # settings.html#topics-settings-ref
        
@ return {None}
'''


def runMultiSpidersINDEPSettings(runconfiglist):
    def prog(runconfiglist):
        argsdict = {
            "runconfiglist": runconfiglist
        }

        logdict = {
            "api_name": runMultiSpidersINDEPSettings.__name__,
            "start_time": getUTCDateTimeObj(),
            "argsdict": argsdict
        }

        apilogutil.api_start(logdict)
        logger.info('calling ' + runMultiSpidersINDEPSettings.__name__)

        m = MultiSpidersProcessor()
        m.runINDEPSettings(runconfiglist)

        logdict['finish_time'] = getUTCDateTimeObj()
        logdict['finish_reason'] = 'api finished normally'

        apilogutil.api_finish(logdict)
        logger.info(runMultiSpidersINDEPSettings.__name__ + ' finished.')

    t = threading.Thread(target=prog,
                         args=(runconfiglist,))
    t.daemon = True
    t.start()