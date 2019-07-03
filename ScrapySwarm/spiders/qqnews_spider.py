#!/usr/bin/python3
'''
@File : qqnews_spider.py

@Time : 2019/6/24

@Author : Boholder

@Function : 腾讯新闻网(news.qq.com)爬虫，需借助百度搜索

            1.腾讯新闻(news.qq.com/a/)分两个排版
            “腾讯新闻事实派” https://news.qq.com/a/20170119/024678.htm
            和“腾讯新闻” https://news.qq.com/a/20100104/000741.htm
            其中发布来源与发布时间的排版还千奇百怪

            2.腾讯网(news.qq.com/omn/)
            https://new.qq.com/omn/NEW20190/NEW2019062500130308.html
            但它不让百度、搜狗索引，所以无从keyword->url list，也就作罢

            百度搜索还可能抓到腾讯新闻网的index网址，此时忽略此条，跳到下一条url

            item['imgs']暂时没有填充，图片是js动态加载的，要写解析挺费劲，先不写
'''

import scrapy
import re

from ScrapySwarm.control.DBAccess \
    import BDsearchUrlUtil

from ScrapySwarm.items import QQNewsItem

from ScrapySwarm.tools.time_format_util \
    import getCurrentTime, formatTimeStr

from ScrapySwarm.control.log_util import SpiderLogUtil


class QQNewsSpider(scrapy.Spider):
    name = 'qqnews_spider'

    def __init__(self, *args, **kwargs):
        # 与BDsearchUrlUtil交互要用的参数，指明网址
        self.site = 'news.qq.com'

        # 需要在parse()中使用该url关联的'keyword'（自定义item属性），
        # 当然 scrapy.response 对象中是没有的，
        # 也不想改写个 response 对象的子类了，直接定义一个类属性
        self.keyword = ''

        self.bd = BDsearchUrlUtil()
        self.slog = SpiderLogUtil()

        super().__init__(*args, **kwargs)

    def close(self, reason):
        # 当爬虫停止时，调用clockoff()修改数据库
        self.slog.spider_finish(self)
        if self.bd.clockoff(self.site, self.keyword):
            self.logger.info('qqnews_spider clock off successful')

        super().close(self, reason)

    def start_requests(self):
        # get params (from console command) when be started
        self.keyword = getattr(self, 'q', None)

        if self.keyword is None:
            self.keyword = '中美贸易'

        self.slog.spider_start(self)

        # get url list for mongoDB
        urllist = self.bd.getNewUrl(self.site, self.keyword)

        # if no new url or error, urllist=None
        if urllist:
            for url in urllist:
                yield scrapy.Request(url, self.parse)

        # # test news_qq spider
        # url = 'https://news.qq.com/a/20170823/002257.htm'
        # yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = QQNewsItem()

        # 两排版通用
        item['url'] = response.url
        item['crawl_time'] = getCurrentTime()
        item['title'] = response.xpath(
            '//div[@class=\'hd\']/h1/text()').get()
        item['keyword'] = self.keyword

        # 正文抽取
        content = ''
        for paragraph in response.xpath(
                '//div[@id=\'Cnt-Main-Article-QQ\']/p/text()'):
            paragraph = paragraph.get().strip()
            paragraph = re.sub(r'<[^i].*?>', '', paragraph)
            paragraph = re.sub(r'\(function[\s\S]+?\}\)\(\);', '', paragraph)
            content = content + paragraph
        item['content'] = content

        # 如果有正文，是新闻，没有，不是
        # 关于发布时间和发布来源的布局我快疯了，区区10年变了好多次布局，要一个个定制
        if content:
            # 发布时间
            item['time'] = self.trygetPublishTime(response)
            # 发布来源
            item['source'] = self.trygetPublishSource(response)

            yield item
        else:
            pass

    @staticmethod
    def trygetPublishTime(response):
        time = response.xpath(
            '//span[@class=\'a_time\']/text()').get()
        if not time:
            time = response.xpath(
                '//div[@class=\'hd\']/div[@bosszone=\'titleDown\']'
                '//span[@class=\'article-time\']/text()').get()
        if not time:
            time = response.xpath(
                '//div[@class=\'info\']/text()').get()
        if not time:
            time = response.xpath(
                '//span[@class=\'pubTime\']/text()').get()

        # 如果时间拿到，格式化时间
        # 两种原格式：
        # 2011年07月12日10:33
        # 2017-08-23 06:30
        # 格式化为：
        # 2017-08-23 06:30
        if time:
            time = formatTimeStr(time)

        return time

    @staticmethod
    def trygetPublishSource(response):
        source = response.xpath(
            '//span[@class=\'a_source\']/a/text()').get()

        if not source:
            source = response.xpath(
                '//span[@class=\'a_source\']/text()').get()

        if not source:
            source = response.xpath(
                '//span[@class=\'where\']/text()').get()

        if not source:
            source = response.xpath(
                '//span[@class=\'where\']/a/text()').get()

        if not source:
            source = response.xpath(
                '//span[@class=\'color-a-1\']/a/text()').get()

        if not source:
            source = response.xpath(
                '//span[@class=\'color-a-1\']/text()').get()

        return source
