# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import scrapy
from scrapy import signals

class ScrapyswarmSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyswarmDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    # driver.get('https://weibo.cn')
    # time.sleep(30)
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def  cookiechange(self,driv,text):
        q=text.split(';')
        for s in q:
            j=s.split('=')
            driv.add_cookie({'name' : j[0], 'value' : j[1]})


    def process_request(self, request, spider):
        # if request.url != 'https://www.aqistudy.cn/historydata/':
        #
        #     # driver.get('https://weibo.cn')
        #     # print(driver.get_cookies())
        #     # # driver.delete_all_cookies()
        #     # self.cookiechange(driver,'_T_WM=f7fc1975334e2610dd77c4a949caaa2e; __guid=78840338.2690867225963806000.1561098303'
        #     #                   '394.3926; TMPTOKEN=xWotEi1ho4BsQadI1WKh50PW3wxeD0MXriFaU01sHfs7ddDfYkc6g8QC0brRQ2iI; SUB=_2A25'
        #     #                   'wCAggDeRhGeBM6lER8yzJzD2IHXVT8qhorDV6PUJbkdAKLUnFkW1NRRuUuWjxLqOlReVo19AJKlLVFf0K-Qcb; SUHB=0h1J3'
        #     #                   'h4MnoA8ye; SCF=AqNspA5hvpJAB-QOIpSEFOvS7uTz2C-xcjU2d4im-izONxHBJbLovO6aDcPk7st0qIDcNhWWOxTPgrhwE'
        #     #                   'NoLpoA.; SSOLoginState=1561098352; monitor_count=2')
        #     self.driver.get(request.url)
        #     print(request.url)
        #     time.sleep(1)
        #     html = self.driver.page_source
        #     return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
        #                                     request=request)
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
