#!/usr/bin/python3
# encoding: utf-8
import os
import time
import re
from lxml import etree
from scrapy import Spider, FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

from ScrapySwarm.control.log_utils import SpiderLogUtil
from ScrapySwarm.items import TweetsItem, InformationItem, RelationshipsItem, CommentItem, ChinaNewsItem


class China(Spider):
    name = "chinanews_spider"
    base_url = "http://sou.chinanews.com/search.do"
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        },
        'CONCURRENT_REQUESTS': 15,
        'DOWNLOAD_DELAY': 2
    }

    def __init__(self, *args, **kwargs):

        self.slog = SpiderLogUtil()

        super().__init__(*args, **kwargs)

    def close(self, reason):

        self.slog.spider_finish(self)
        super().close(self, reason)

    def start_requests(self):

        querystr = getattr(self, 'q', None)
        if not querystr:
            querystr = '中美贸易'
        self.querystr = querystr
        self.q = []
        # folderpath ='E:\chinanews' + querystr
        # if (not os.path.exists(folderpath)):
        #     os.mkdir(folderpath)

        self.slog.spider_start(self)

        my_data = {'q': querystr,
                   'ps': '10',
                   'start': '0',
                   'type': '',
                   'sort': 'pubtime',
                   'time_scope': str(0),
                   'channel': 'all',
                   'adv': str(1),
                   'day1': '',
                   'day2': '',
                   'field': '',
                   'creator': ''}
        yield FormRequest(formdata=my_data, url=self.base_url,
                          callback=self.parsefornum, )

    def parsefornum(self, response):
        body = response.body
        body = body.decode("utf-8")
        response.replace(body=body)
        pre = re.compile(r'ongetkey\((\d+)\).?>尾页')
        num=pre.findall(str(body))
        num=int(num[0])
        print(num)
        if num>400:
            num=400
        for i in range(num):
            q = i * 10
            my_data = {'q': self.querystr,
                       'ps': '10',
                       'start': str(q),
                       'type': '',
                       'sort': 'pubtime',
                       'time_scope': str(0),
                       'channel': 'all',
                       'adv': str(1),
                       'day1': '',
                       'day2': '',
                       'field': '',
                       'creator': ''}
            yield FormRequest(formdata=my_data, url=self.base_url,
                              callback=self.parse, )



    def parse(self, response):
        body = response.body
        body = body.decode("utf-8")
        response.replace(body=body)
        for div in response.xpath('//td/ul/li[@class="news_title"]/a/@href'):
            url = div.extract()
            yield Request(url=url, callback=self.parse2)


    def parse2(self, response):
        body = response.body

        body = body.decode("utf-8", "ignore")

        response.replace(body=body)
        item = ChinaNewsItem()

        title = response.xpath('//div[@class="content"]/h1/text()').get()
        if title:
            title=title.strip();

            imgs = []
            content = ''
            ire = re.compile(r'src=\"(.+?)\"')
            pre = re.compile(r'<img[\s\S]+?>')
            url = response.url
            for p in response.xpath('//div[@class="left_zw"]').extract():
                p = re.sub(r'<[^i].*?>', '', p)
                p = re.sub(r'\(function[\s\S]+?\}\)\(\);', '', p)
                q = pre.findall(p)
                for i in q:
                    imgs.append(ire.findall(i)[0])
                    p = p.replace(i, '&&此处有图片，url:' + imgs[-1] + ",存储名为:" + (url.split('/')[-1]) + imgs[-1].split('/')[
                        -1] + '&&')
                content = content + p.strip()
            timeandsource = response.xpath('//div[@class="left-t"]/text()').get().strip()
            ts = timeandsource.split('来源')

            item['crawl_time'] = str(int(time.time()))
            created_time = ts[0].strip()
            timeArray = time.strptime(created_time, "%Y年%m月%d日 %H:%M")
            otherStyleTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
            item['source'] = '中国新闻'
            if len(ts) > 1:
                source = ts[1]
                item['source'] = source

            item['keyword'] = self.querystr
            item['title'] = title
            item['content'] = content.replace("\r","").replace("\n","")
            item['time'] = otherStyleTime
            item['url'] = url
            item['imgs'] = imgs
            yield item


# if __name__ == "__main__":
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('chinanews_spider')
#     process.start()