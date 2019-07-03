#!/usr/bin/python3
'''
@File : spider_exist_util.py

@Time : 2019/7/2

@Author : Boholder

@Function : tell if a spider exist in project or it's type

'''
from ScrapySwarm.settings import BDA_SPIDERS, DIRC_SPIDERS
from scrapy import spiderloader
from scrapy.utils import project


def exist(spidername):
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]

    flag = False
    for c in classes:
        if spidername == c.name:
            flag = True
    if flag:
        return True
    else:
        return False


def isBDAType(spidername):
    flag = False
    for name in BDA_SPIDERS:
        if spidername == name:
            flag = True
    if flag:
        return True
    else:
        return False