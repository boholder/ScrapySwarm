#!/usr/bin/python3
'''
@File : swarm_api.py

@Time : 2019/7/1

@Author : Boholder

@Function : API for upper system to
            run spider, read swarm's log etc.

'''
from ScrapySwarm.control.spider_run_control import *
from ScrapySwarm.tools.spider_exist_util import *

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

'''


def runOneSpider(spidername, keyword,
                 log=True, settings=None):

    # judge spidername exist in project or not
    # Spider.name MUST equal to python file name
    # due to implement method
    if not exist(spidername):
        return False

    # judge spider's type (baidu assist OR direct url)
    if isBDAType(spidername):
        processor = BDAssistSpiderProcessor()
    else:
        processor = DirectUrlSpiderProcessor()

    # run it, stuck until get return
    logfilename = processor.run(spidername, keyword,
                                log, False, settings)

    # return this process's log (by reading log file)
    # or return a bool
    if type(logfilename) == str:
        logfile = open(logfilename, 'r')
        loglist=[]

        while logfile:
            loglist.append(logfile.readline())

        return loglist

    else:
        return True

'''
Just run all spiders that can be ran.

@ param {str} keyword: only need it to config spider

@ return {None}
'''


def runAllSpider(keyword):
    m=MultiSpidersProcessor()
    m.runAll(keyword)