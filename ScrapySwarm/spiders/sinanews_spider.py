#!/usr/bin/python3
'''
@File : sinanews_spider.py

@Time : 2019/6/25

@Author : Boholder

@Function : 【借助百度搜索】，爬取最新布局的新浪新闻 exm:
            https://news.sina.com.cn/c/2019-06-24/doc-ihytcitk7355640.shtml

            感谢新浪前端开发者，
            即使url因新闻分类各不相同，布局还是统一的，省大事了。

            为什么要借助百度，因为新浪内置的新浪搜索不能完美地执行
            "选定关键字全包含" 参数，即使它确实在高级搜索确实定义了。
            当然，也省得再写个爬虫了。
'''

import scrapy
import re

from ScrapySwarm.control.DBAccess \
    import BDsearchUrlUtil

from ScrapySwarm.items import SinaNewsItem

from ScrapySwarm.tools.time_format_util \
    import getCurrentTime, formatTimeStr

from ScrapySwarm.control.log_utils import SpiderLogUtil


class SinaNewsSpider(scrapy.Spider):
    name = 'sinanews_spider'

    def __init__(self, *args, **kwargs):
        # 与BDsearchUrlUtil交互要用的参数，指明网址
        self.site = 'news.sina.com.cn'

        # 需要在parse()中使用该url关联的'keyword'（自定义item属性），
        # 当然 scrapy.response 对象中是没有的，
        # 也不想改写个 response 对象的子类了，直接定义一个类属性
        self.keyword = ''

        self.bd = BDsearchUrlUtil()

        self.slog = SpiderLogUtil()

        super().__init__(*args, **kwargs)

    def close(self, reason):
        self.slog.spider_finish(self)

        # 当爬虫停止时，调用clockoff()修改数据库
        if self.bd.clockoff(self.site, self.keyword):
            self.logger.info('sinanews_spider clock off successful')

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

        # # test spider
        # url = 'http://news.sina.com.cn/c/2019-06-24' \
        #       '/doc-ihytcitk7355640.shtml'
        # yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = SinaNewsItem()

        item['url'] = response.url
        item['crawl_time'] = getCurrentTime()
        item['keyword'] = self.keyword

        title = response.xpath(
            '//title/text()').get()
        if title:
            title = title.replace('_新浪新闻', '')
            title = title.replace('_新浪网', '')
            title = title.replace('_新浪军事', '')
            title = title.replace('_新闻中心', '')
        item['title'] = title

        item['time'] = self.trygetPublishTime(response)

        item['source'] = self.trygetPublishSource(response)

        # 正文抽取

        item['content'] = self.trygetContent(response)

        yield item

    @staticmethod
    def trygetPublishTime(response):
        time = response.xpath(
            '//div[@class=\'date-source\']'
            '/span[@class=\'date\']/text()').get()

        # http://news.sina.com.cn/o/2017-07-07/doc-ifyhvyie0474852.shtml
        # http://mil.news.sina.com.cn/china/2016-04-14/
        # doc-ifxriqqx2384948.shtml
        if not time:
            if response.xpath(
                    '//span[@class=\'time-source\']'
                    '//span[@class=\'titer\']'):
                time = response.xpath(
                    '//span[@class=\'time-source\']'
                    '//span[@class=\'titer\']/text()').get()
            else:
                time = response.xpath(
                    '//span[@class=\'time-source\']/text()').get()
                if time:
                    time = re.sub(r'<[^i].*?>', '', time)

        if time:
            timefmt = formatTimeStr(time)
            if timefmt:
                return timefmt
            else:
                return time
        else:
            return None

    @staticmethod
    def trygetPublishSource(response):
        source = response.xpath(
            '//div[@class=\'date-source\']'
            '/a[@class=\'source\']/text()').get()
        # http://news.sina.com.cn/o/2017-07-07/doc-ifyhvyie0474852.shtml
        if not source:
            source = response.xpath('//div[@class=\'time-source\']'
                                    '//a/text()').get()

        # http://mil.news.sina.com.cn/china/
        # 2016-04-14/doc-ifxriqqx2384948.shtml
        if not source:
            source = response.xpath('//span[@class=\'time-source\']'
                                    '//span[@class=\'source\']'
                                    '/text()').get()

        return source

    @staticmethod
    def trygetContent(response):
        content = ''

        def paragraph_process(paragraph):
            p = paragraph.get().strip()
            p = re.sub(r'<[^i].*?>', '', p)
            p = re.sub(r'\(function[\s\S]+?\}\)\(\);', '', p)
            return p

        # /a/ /c/ doc-... /o/
        if response.xpath(
                '//div[@id=\'article\']//p/text()'):

            for paragraph in response.xpath(
                    '//div[@id=\'article\']//p/text()'):
                content = content + paragraph_process(paragraph)

        # some of /o/
        # http://news.sina.com.cn/o/2019-05-14/doc-ihvhiews1782968.shtml
        elif response.xpath(
                '//div[@id=\'article\']//p/text()'):

            for paragraph in response.xpath(
                    '//div[@id=\'article\']//div/text()'):
                content = content + paragraph_process(paragraph)

        # http://news.sina.com.cn/o/2017-07-07/doc-ifyhvyie0474852.shtml
        elif response.xpath('//div[@id=\'artibody\']//p/text()'):
            for paragraph in response.xpath(
                    '//div[@id=\'artibody\']//p/text()'):
                content = content + paragraph_process(paragraph)

        return content
