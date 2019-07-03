#!/usr/bin/python3
'''
@File : debug.py

@Time : 2019/6/23

@Author : Boholder

@Function : 

'''
# # crawl sinanews -a q=中朝贸易
# from scrapy.cmdline import execute
# execute()

from ScrapySwarm.control.swarm_api import *
runOneSpider('qqnews_spider','中朝贸易', False)
print('aaa')


# import copy
#
# from scrapy import spiderloader
# from scrapy.utils import project
#
# settings = project.get_project_settings()
# spider_loader = spiderloader.SpiderLoader.from_settings(settings)
# spiders = spider_loader.list()
# classes = [spider_loader.load(name) for name in spiders]
# print(classes[0].name)
#
# a=copy.deepcopy(project.get_project_settings())
# pass