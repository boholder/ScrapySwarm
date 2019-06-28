#!/usr/bin/python3
'''
@File : time_format_util.py

@Time : 2019/6/24

@Author : Boholder

@Function : 将所有表示时间的变量统一整理为项目规定的
            ‘YYYY-MM-DD-HH-MM-SS’ 格式

'''
import datetime
import time

'''
返回被调用时的系统时间

@ return {int} format: millisecond
'''


def getCurrentTime():
    return int(time.time())


'''

'''


def getCurrentTimeReadable():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


'''

'''


def getUTCDateTimeObj():
    return datetime.datetime.utcnow()

'''
2011年07月12日10:33
2019年06月21日 17:38
2017-08-23 06:30
-> YYYY-MM-DD-HH-MM-SS
'''

def formatTimeStr(time):
    # time exm: 2017-08-23 06:30
    if time[4] == '-':
        time = time.replace(' ', '-') \
                   .replace(':', '-') + '-00'

    # 2011年...
    if time[4] == '年':
        # 2019年06月21日 17:38
        if time[11] == ' ':
            time = time.replace('年', '-') \
                       .replace('月', '-') \
                       .replace('日 ', '-') \
                       .replace(':', '-') + '-00'
        # 2011年07月12日10:33
        else:
            time = time.replace('年', '-') \
                       .replace('月', '-') \
                       .replace('日', '-') \
                       .replace(':', '-') + '-00'
    return time