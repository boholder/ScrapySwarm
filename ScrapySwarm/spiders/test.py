#!/usr/bin/python3
'''
@File : test.py

@Time : 2019/6/23

@Author : Boholder

@Function : 

'''
from ScrapySwarm.spiders.bdsearch_url_util import BDsearchUrlUtil as bd

util=bd()

a = util.getNewUrl('news.qq.com','2019-06-23-14-55-53')
print(a)