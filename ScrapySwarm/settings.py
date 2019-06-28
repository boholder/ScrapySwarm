# -*- coding: utf-8 -*-

# Scrapy settings for ScrapySwarm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ScrapySwarm'
COMMANDS_MODULE = 'ScrapySwarm.control'
SPIDER_MODULES = ['ScrapySwarm.spiders']
NEWSPIDER_MODULE = 'ScrapySwarm.spiders'

# MongoDB setting
LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017

# data db & collections name
MONGO_DB_NAME = 'WebData'
COLL_BAIDU_SREACH = 'baidu_search_results'
COLL_WEIBO_INFOMATION = 'weibo_infomation'
COLL_WEIBO_TWEETS = 'weibo_tweets'
COLL_WEIBO_COMMENTS = 'weibo_comments'
COLL_WEIBO_RELATIONSHIPS = 'weibo_relationships'
COLL_CHINA_NEWS = 'news_china'
COLL_QQ_NEWS = 'news_qq'
COLL_SINA_NEWS = 'news_sina'

# log db & collections name
LOG_DB_NAME = 'SwarmLog'
COLL_SPIDERS_LOG = 'spiders_log'
COLL_API_LOG = 'api_log'

ITEM_PIPELINES = {'ScrapySwarm.pipelines.ScrapyswarmPipeline': 300, }

#
# SPIDER_MIDDLEWARES = {
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

# 渲染服务的url
# SPLASH_URL = 'http://192.168.99.100:8050'
#
# DOWNLOADER_MIDDLEWARES = {
#    'scrapy_splash.SplashCookiesMiddleware': 723,
#    'scrapy_splash.SplashMiddleware': 725,
#    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
#
# }
# # 去重过滤器
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# # 使用Splash的Http缓存
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


# ===weibo setting===

# 请将Cookie替换成你自己的Cookie
# DEFAULT_REQUEST_HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#     # 'Cookie':'cnsuuid=0c227bee-6417-bd3b-d284-e0f787ac865f1379.9189296160002_1545061950996; UM_distinctid=168070e584a209-0a2cefadf46d62-3c604504-1fa400-168070e584b5a2; cn_1263394109_dplus=%7B%22distinct_id%22%3A%20%22168070e584a209-0a2cefadf46d62-3c604504-1fa400-168070e584b5a2%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201546306963%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201546306963%7D%7D; JSESSIONID=aaadmhsH0VDqudBic18Tw; __cdnuid=1160f992ba462f7993c74d52189484e1; __guid=4998577.636917693065358700.1561167132049.0295; Hm_lvt_0da10fbf73cda14a786cd75b91f6beab=1558685555,1561179103; zycna=fYamWwlwALsBATrCqK2zi68i; Hm_lpvt_0da10fbf73cda14a786cd75b91f6beab=1561182136; monitor_count=22'
#     'Cookie':'_T_WM=f7fc1975334e2610dd77c4a949caaa2e; __guid=78840338.2690867225963806000.1561098303394.3926; TMPTOKEN=xWotEi1ho4BsQadI1WKh50PW3wxeD0MXriFaU01sHfs7ddDfYkc6g8QC0brRQ2iI; SUB=_2A25wCAggDeRhGeBM6lER8yzJzD2IHXVT8qhorDV6PUJbkdAKLUnFkW1NRRuUuWjxLqOlReVo19AJKlLVFf0K-Qcb; SUHB=0h1J3h4MnoA8ye; SCF=AqNspA5hvpJAB-QOIpSEFOvS7uTz2C-xcjU2d4im-izONxHBJbLovO6aDcPk7st0qIDcNhWWOxTPgrhwENoLpoA.; SSOLoginState=1561098352; monitor_count=2'
# }
#
# # 当前是单账号，所以下面的 CONCURRENT_REQUESTS �DOWNLOAD_DELAY 请不要修�
#
# CONCURRENT_REQUESTS = 16
#
# DOWNLOAD_DELAY = 3
#
# DOWNLOADER_MIDDLEWARES = {
#     'weibo.middlewares.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
# }
#
# ITEM_PIPELINES = {
#     'sina.pipelines.MongoDBPipeline': 300,
# }
# ===weibo setting END===

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ScrapySwarm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ScrapySwarm.middlewares.ScrapyswarmSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'ScrapySwarm.middlewares.ScrapyswarmDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'ScrapySwarm.pipelines.ScrapyswarmPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
