#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@File : baidu_search_spider.py

@Time : 2019/6/22

@Author : Boholder

@Function : 使用百度搜索，对指定关键字，指定网站进行站内搜索，
            并收集返回的url，以供下一步网站定制spider搜索
'''
import scrapy
import re
import time
from ScrapySwarm.items import BaiduSearchItem

class BaiduSearchSpider(scrapy.Spider):
    name = 'baidusearch'

    def start_requests(self):
        # get params (from console command) when be started
        querystr = getattr(self, 'q', None)
        site = getattr(self, 'site', None)

        if querystr is None:
            querystr = '中美贸易'
        if site is None:
            site = 'news.qq.com'
        url = self.baidusearchurlGen(self, querystr, site, 0)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # ===get info from every result===
        for oneresult in response.xpath('//div[@class=\'result c-container \']\
                                    /h3/a/@href'):
            item = BaiduSearchItem()
            item['url'] = oneresult.get()
            item['crawl_time'] = self.getCurrentTime(self)
            item['site'] = self.getOriSiteUrl(self, response.url)
            yield item

        # ===crawl next page, if exist===

        # pn = page number
        currentpn = response.xpath('//div[@id=\'page\']/\
                        strong/span[@class=\'pc\']/text()')
        if currentpn:
            currentpn = int(currentpn[0].get())

        maxpn = response.xpath('//div[@id=\'page\']/a\
                        /span[@class=\'pc\']/text()')
        if maxpn:
            maxpn = int(maxpn[-1].get())

        nextpn = None

        # if so, exist one page num bigger than current page num
        if (currentpn and maxpn and (maxpn > currentpn)):
            nextpn = currentpn + 1

        if nextpn:
            # get '...&pn=' sub string
            pncharindex = re.search('&pn=', response.url).span()[1]
            nexturl = response.url[:pncharindex] + str((nextpn - 1) * 10)
            yield response.follow(nexturl, self.parse)

    '''
    百度搜索的url的构建函数，以作为种子url列表供爬虫使用
        exm: http://www.baidu.com/s?wd="中美贸易" site%3Anews.qq.com&pn=0
            原查询词： ("中美贸易" site:news.qq.com)
            pn: page number,本页第一条结果在结果排行中的位置。
                pn = ${结果页码-1}*rn
                但rn参数(每页结果条数)已经反应不正常了，
                所以就是默认每页十条。
    
    @ param {string} querystr 查询字符串   exm:中美贸易
    
    @ param {string} site     exm:news.qq.com
                                借用百度的site搜索属性搜索某站内
                                
    @ param {string} pagenumber 本页第一条结果,=pn
    
    @ return {string}         exm: https://www.baidu.com/s?
                                wd="中美贸易" site%3Anews.qq.com&pn=0
    '''

    @staticmethod
    def baidusearchurlGen(self, querystr, site, pagenumber):
        # 注意https 有一个防爬虫机制，脚本加载真正数据，只能爬个壳。
        return "http://www.baidu.com/s?wd=\"" \
               + querystr + "\" site:" + site + "&pn=" + str(pagenumber)

    '''
    返回被调用时的系统时间
    
    @ return {string} format: YYYY-MM-DD-HH-MM-SS
    '''

    @staticmethod
    def getCurrentTime(self):
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    '''
    获取搜索时的原站点网址 exm: news.qq.com
    
    @ param {string} resurl response.url 
                            exm: https://www.baidu.com/s?
                                wd="中美贸易" site%3Anews.qq.com&pn=0
                                
    @ return {string}
    '''

    @staticmethod
    def getOriSiteUrl(self, resurl):
        # 'site%3A{site domain}&pn'
        sitecharindex = re.search('site:.*&pn', resurl).span()
        strstart = int(sitecharindex[0]) + 5
        strend = int(sitecharindex[1]) - 3
        # '{site domain}'
        return resurl[strstart:strend]
