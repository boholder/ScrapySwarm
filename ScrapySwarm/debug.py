#!/usr/bin/python3
'''
@File : debug.py

@Time : 2019/6/23

@Author : Boholder

@Function : 

'''
from scrapy.cmdline import execute
execute()

import ScrapySwarm.tools.time_format_util as t
from ScrapySwarm.control.log_util import spider_log_util
import ScrapySwarm.spiders.qqnews_spider as qq

# s=qq()
#
# a=spider_log_util()
# a.spider_start(s)