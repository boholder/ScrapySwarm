#!/usr/bin/python3
# encoding: utf-8
import json
import re
from lxml import etree
from scrapy import Spider, FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from ScrapySwarm.items import TweetsItem, InformationItem, RelationshipsItem, CommentItem, ChinaNewsItem
from ScrapySwarm.spiders.weibo_utils import time_fix, extract_weibo_content, extract_comment_content
import time


class China(Spider):
    name = "chinanews_spider"
    base_url = "http://sou.chinanews.com/search.do"

    q = []

    def start_requests(self):
        # start_uids = [
        #     '2803301701',  # 人民日报
        #     '1699432410'  # 新华社
        # ]
        for i in range(300):
            q=i*10
            my_data = {'q': '中美贸易',
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
            yield FormRequest(formdata=my_data,url=self.base_url,
                           callback=self.parse, )

    def parse(self, response):
        body = response.body
        body = body.decode("utf-8")
        # print(body)
        response.replace(body=body)
        # with open('/response', 'w') as f:
        #     f.write(str(response.body))
        for  div in response.xpath('//td/ul/li[@class="news_title"]/a/@href'):
            url=div.extract()
            print(url)
            yield Request(url=url, callback=self.parse2 )

    def parse2(self, response):
        body = response.body

        body = body.decode("utf-8","ignore")
        # print(body)
        # print(body)
        response.replace(body=body)
        # with open('/response', 'w') as f:
        #     f.write(str(response.body))
        item=NewsItem()

        title=response.xpath('//div[@class="content"]/h1/text()').get().strip();
        content=''
        for p in response.xpath('//div[@class="left_zw"]/p/text()'):
            content=content+p.get().strip()

        time=response.xpath('//div[@class="left-t"]/text()').get().replace('来源：',"").strip()
        url=response.url
        item['title']=title
        item['content']=content
        item['time']=time
        item['url']=url
        print(title,content,time,url)
        yield item




if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('chinanews_spider')
    process.start()