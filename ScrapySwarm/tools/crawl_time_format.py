#!/usr/bin/python3
'''
@File : crawl_time_format.py

@Time : 2019/6/24

@Author : Boholder

@Function : 将所有表示时间的变量统一整理为项目规定的
            ‘YYYY-MM-DD-HH-MM-SS’ 格式

'''

import time

'''
返回被调用时的系统时间

@ return {string} format: 'YYYY-MM-DD-HH-MM-SS'
'''


def getCurrentTime():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())