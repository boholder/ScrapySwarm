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
import urllib.parse

from ScrapySwarm.items import BaiduSearchItem

from ScrapySwarm.tools.time_format_util import getCurrentTime

from ScrapySwarm.control.log_util import SpiderLogUtil

class BaiduSearchSpider(scrapy.Spider):
    name = 'baidu_search_spider'

    def __init__(self, *args, **kwargs):

        self.slog = SpiderLogUtil()

        super().__init__(*args, **kwargs)

    def close(self, reason):

        self.slog.spider_finish(self)
        super().close(self, reason)

    def start_requests(self):
        # get params (from console command) when be started
        querystr = getattr(self, 'q', None)
        site = getattr(self, 'site', None)

        if querystr is None:
            querystr = '中美贸易'
        if site is None:
            site = 'news.qq.com'

        self.slog.spider_start(self)

        url = self.baidusearchurlGen(querystr, site, 0)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        # if no result, quit spider
        if response.xpath('//div[@class=\'content_none\']'):
            return

        # ===get info from every result===
        for oneresult in response.xpath('//div[@class=\'result c-container \']\
                                    /h3/a/@href'):
            item = BaiduSearchItem()
            item['url'] = oneresult.get()
            item['crawl_time'] = getCurrentTime()
            item['site'] = self.getOrigSiteUrl(response.url)
            item['waste'] = 0
            item['keyword'] = self.getOrigKeyword(response.url)
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
    def baidusearchurlGen(querystr, site, pagenumber):
        # 注意https 有一个防爬虫机制，脚本加载真正数据，只能爬个壳。
        return "http://www.baidu.com/s?wd=\"" \
               + querystr + "\" site:" + site + "&pn=" + str(pagenumber)

    '''
    获取搜索时的原站点网址 exm: news.qq.com
    
    @ param {string} resurl response.url 
                            exm: https://www.baidu.com/s?
                                wd="中美贸易" site%3Anews.qq.com&pn=0
                                
    @ return {string}
    '''

    @staticmethod
    def getOrigSiteUrl(resurl):
        # 'site%3A{site domain}&pn'
        index = re.search('site:.*&pn', resurl).span()
        # '{site domain}'
        return resurl[(index[0] + 5):(index[1] - 3)]


    '''
    获取搜索时的关键字 exm: ‘中美贸易’

    @ param {string} resurl response.url 
                            exm: https://www.baidu.com/s?
                                wd=中美贸易 site%3Anews.qq.com&pn=0

    @ return {string}
    '''

    @staticmethod
    def getOrigKeyword(resurl):
        # 's?wd="{keyword}" site'
        index = re.search('wd=%22.*%22%20', resurl).span()
        # '{keyword} in url(ascii for url), decode'
        return urllib.parse.unquote(resurl[(index[0] + 6):(index[1] - 6)])
