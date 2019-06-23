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
    custom_settings = {
        # 请将Cookie替换成你自己的Cookie
        # 'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            # 'Cookie':'cnsuuid=0c227bee-6417-bd3b-d284-e0f787ac865f1379.9189296160002_1545061950996; UM_distinctid=168070e584a209-0a2cefadf46d62-3c604504-1fa400-168070e584b5a2; cn_1263394109_dplus=%7B%22distinct_id%22%3A%20%22168070e584a209-0a2cefadf46d62-3c604504-1fa400-168070e584b5a2%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201546306963%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201546306963%7D%7D; JSESSIONID=aaadmhsH0VDqudBic18Tw; __cdnuid=1160f992ba462f7993c74d52189484e1; __guid=4998577.636917693065358700.1561167132049.0295; Hm_lvt_0da10fbf73cda14a786cd75b91f6beab=1558685555,1561179103; zycna=fYamWwlwALsBATrCqK2zi68i; Hm_lpvt_0da10fbf73cda14a786cd75b91f6beab=1561182136; monitor_count=22'
        },
        'CONCURRENT_REQUESTS' : 16,
        'DOWNLOAD_DELAY' : 3
    }
    q = []

    def start_requests(self):
        # start_uids = [
        #     '2803301701',  # 人民日报
        #     '1699432410'  # 新华�
        # ]
        for i in range(300):
            q = i * 10
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
            yield FormRequest(formdata=my_data, url=self.base_url,
                              callback=self.parse, )

    def parse(self, response):
        body = response.body
        body = body.decode("utf-8")
        # print(body)
        response.replace(body=body)
        # with open('/response', 'w') as f:
        #     f.write(str(response.body))
        for div in response.xpath('//td/ul/li[@class="news_title"]/a/@href'):
            url = div.extract()
            print(url)
            yield Request(url=url, callback=self.parse2)

    def parse2(self, response):
        body = response.body

        body = body.decode("utf-8", "ignore")
        # print(body)
        # print(body)
        response.replace(body=body)
        # with open('/response', 'w') as f:
        #     f.write(str(response.body))
        item = ChinaNewsItem()

        title = response.xpath('//div[@class="content"]/h1/text()').get().strip();

        imgs=[]
        content = ''
        ire=re.compile(r'src=\"(.+?)\"')
        pre = re.compile(r'<img[\s\S]+?>')
        url = response.url
        for p in response.xpath('//div[@class="left_zw"]').extract():
            p = re.sub(r'<[^i].*?>','',p)
            p = re.sub(r'\(function[\s\S]+?\}\)\(\);' , '', p)
            q =pre.findall(p)
            for i in q :
                imgs.append(ire.findall(i)[0])
                p=p.replace(i,'&&此处有图片，url:'+imgs[-1]+",存储名为:"+(url.split('/')[-1])+imgs[-1].split('/')[-1]+'&&')
            content = content + p.strip()
        time = response.xpath('//div[@class="left-t"]/text()').get().replace('来源', "").strip()

        item['title'] = title
        item['content'] = content
        item['time'] = time
        item['url'] = url
        item['imgs']=imgs
        print(title, content, time, url)
        yield item


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('chinanews_spider')
    process.start()
