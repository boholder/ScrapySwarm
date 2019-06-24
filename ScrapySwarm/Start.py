from scrapy import cmdline



def startCrawl(keyword):
    if not keyword:
        keyword="中美贸易"
    cmdline.execute(("scrapy crawl chinanews_spider -a q="+keyword).split())
    # cmdline.execute(("scrapy crawl weibo_spider -a q=" + keyword).split())

startCrawl("")