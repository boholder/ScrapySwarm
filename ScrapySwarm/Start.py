import os
import threading
import time

from scrapy import cmdline



def startCrawl(keyword):
    if not keyword:
        keyword="中美贸易"

    # os.system(("scrapy crawll chinanews_spider -a q=" + keyword))
    #
    # for i in range(4):
    #
    #     os.system(("scrapy crawl weibo_spider -a q=" + keyword))
    # os.system(("scrapy crawl weibo_spider -a q=" + keyword+' -a comments='))
    # while True:
    #     time.sleep(6)

    # #同时运行所有爬虫
    os.system(("scrapy command  weibo_spider  -a q=" + keyword ))


startCrawl("蔡徐坤")