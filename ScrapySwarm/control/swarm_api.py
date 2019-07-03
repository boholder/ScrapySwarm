#!/usr/bin/python3
'''
@File : swarm_api.py

@Time : 2019/7/1

@Author : Boholder

@Function : API for upper system to
            run spider, read swarm's log etc.

'''
import logging

from ScrapySwarm.control.spider_run_control import *
from ScrapySwarm.tools.spider_exist_util import *
from ScrapySwarm.control.log_util import APILogUtil
from ScrapySwarm.tools.time_format_util import getUTCDateTimeObj

'''
Run one spider in project, get process's log in return

@ param {str} spidername: spider class 'name' variable

@ param {str} keyword: keyword for search in the site

@ param {bool} log: True(default), output log into a file
                    False, log settings obey 'settings' param
                    see 
    https://docs.scrapy.org/en/latest/topics/settings.html#log-file
                    for more

@ param {dict} settings: same as above

@ return {bool} if no log file generated, return process result
         {list} log text, one index per line
         {None} something throw error inside file I/O code

'''
apilogutil = APILogUtil()

logger=logging.getLogger(__name__)

def runOneSpider(spidername, keyword,
                 log=True, settings=None):
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

    logger.info('calling '+runOneSpider.__name__)
    apilogutil.api_start(logdict)

    # judge spidername exist in project or not
    # Spider.name MUST equal to python file name
    # due to implement method
    if not exist(spidername):
        logdict['finish_reason'] = \
            'given spider name not found under \'spider\' dir' \
            '(it may because spider\'s name var ' \
            'not equal to class file\'s name)'
        apilogutil.api_finish(logdict)
        logger.info(runOneSpider.__name__ + ' finished.')

        return False

    # judge spider's type (baidu assist OR direct url)
    if isBDAType(spidername):
        processor = BDAssistSpiderProcessor()
    else:
        processor = DirectUrlSpiderProcessor()

    # run it, stuck until get return
    logfilename = processor.run(spidername, keyword,
                                log, None, settings)

    logdict['finish_time'] = getUTCDateTimeObj()

    # return this process's log (by reading log file)
    # or return a bool
    if type(logfilename) == str:
        try:
            logfile = open(logfilename, 'r')
            loglist = []

            while logfile:
                loglist.append(logfile.readline())

            logdict['finish_reason'] = 'api finished normally.'
            apilogutil.api_finish(logdict)
            logger.info(runOneSpider.__name__ + ' finished.')

            return loglist
        except IOError:
            logdict['finish_reason'] = \
                'spider run finished, ' \
                'but can\' t open expect log file' \
                '(I/O error threw).'
            apilogutil.api_finish(logdict)
            logger.info(runOneSpider.__name__ + ' finished.')
            return None

    else:
        return True


'''
Just run all spiders that can be ran.

@ param {str} keyword: only need it to config spider

@ return {None}
'''


def runAllSpider(keyword):
    argsdict={
        "keyword":keyword
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

    logdict['finish_time']=getUTCDateTimeObj()
    logdict['finish_reason']='api finished normally'

    apilogutil.api_finish(logdict)
    logger.info(runAllSpider.__name__ + ' finished.')

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

# '''
# Run more than one spiders with same given settings
# (but not default settings)
# '''
