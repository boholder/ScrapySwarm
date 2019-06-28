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

from ScrapySwarm.tools.DBAccess \
    import BDsearchUrlUtil

from ScrapySwarm.items import SinaNewsItem

from ScrapySwarm.tools.time_format_util \
    import getCurrentTime, formatTimeStr

from ScrapySwarm.control.log_util import spider_log_util


class SinaNewsSpider(scrapy.Spider):
    name = 'sinanews'

    def __init__(self, *args, **kwargs):
        # 与BDsearchUrlUtil交互要用的参数，指明网址
        self.site = 'news.sina.com.cn'

        # 需要在parse()中使用该url关联的'keyword'（自定义item属性），
        # 当然 scrapy.response 对象中是没有的，
        # 也不想改写个 response 对象的子类了，直接定义一个类属性
        self.keyword = ''

        self.bd = BDsearchUrlUtil()

        self.slog = spider_log_util()

        super().__init__(*args, **kwargs)

    def close(self, reason):
        self.slog.spider_finish(self)

        # 当爬虫停止时，调用clockoff()修改数据库
        if self.bd.clockoff(self.site, self.keyword):
            self.logger.info('SinaNews_spider clock off successful')

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

        item['title'] = response.xpath(
            '//h1[@class=\'main-title\']/text()').get()

        time = response.xpath(
            '//div[@class=\'date-source\']'
            '/span[@class=\'date\']/text()').get()
        item['time'] = formatTimeStr(time)

        item['source'] = response.xpath(
            '//div[@class=\'date-source\']'
            '/a[@class=\'source\']/text()').get()

        # 正文抽取
        content = ''

        # /a/ /c/ doc-... /o/
        if response.xpath(
                '//div[@id=\'article\']//p/text()'):

            for paragraph in response.xpath(
                    '//div[@id=\'article\']//p/text()'):
                paragraph = paragraph.get().strip()
                paragraph = re.sub(r'<[^i].*?>', '', paragraph)
                paragraph = re.sub(r'\(function[\s\S]+?\}\)\(\);', '', paragraph)
                content = content + paragraph

        # some of /o/
        # http://news.sina.com.cn/o/2019-05-14/doc-ihvhiews1782968.shtml
        elif response.xpath(
                '//div[@id=\'article\']//p/text()'):

            for paragraph in response.xpath(
                    '//div[@id=\'article\']//div/text()'):
                paragraph = paragraph.get().strip()
                paragraph = re.sub(r'<[^i].*?>', '', paragraph)
                paragraph = re.sub(r'\(function[\s\S]+?\}\)\(\);', '', paragraph)
                content = content + paragraph

        item['content'] = content

        yield item
