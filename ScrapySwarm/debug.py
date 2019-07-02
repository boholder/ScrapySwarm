#!/usr/bin/python3
'''
@File : debug.py

@Time : 2019/6/23

@Author : Boholder

@Function : 

'''
# from scrapy.cmdline import execute
# execute()

from ScrapySwarm.control.spider_run_control import *

a=MultiSpidersProcessor()
a.runAll('中朝贸易')