# Database Structure
# 数据库结构

## 前言

本程序使用 [MongoDB](https://www.mongodb.com/) 作为数据库支持，  
[pymongo](https://api.mongodb.com/python/current/) 库作为语言级DB驱动。

运行本程序需要 **提前** 构建两个数据库：WebData，与 SwaemLog。  
WebData 为爬虫抓取到的数据。  
SwaemLog 为爬虫与爬虫主控API的日志。

集合间无关系，E-R图免了画。

## 目录

* [1. DB: WebData](#1-db-webdata)
	* [1.1. Collections](#11-collections)
	* [1.2. DB Dictionary](#12-dbdictionary)
		* [1.2.1 baidu_search_results](#121-baidu_search_results)
		* [1.2.2 news collections](#122-newscollections)
		* [1.2.3 weibo_comment](#123-weibo_comment)
		* [1.2.4 weibo_infomation](124-weibo_infomation)
		* [1.2.5 weibo_tweets](125-weibo_tweets)
* [2. DB: SwarmLog](#2-db-swarmlog)
	* [2.1 Collections](#21-collections)	
	* [1.2. DB Dictionary](#22-dbdictionary)
		* [2.2.1 api_log](#221-api_log)
		* [2.2.2 spiders_log](#222-spiders_log)
		* [2.2.3 keyword_statistics](#223-keyword_statistics)
		

## 1. DB: WebData

### 1.1. Collections

* baidu_search_results

	[百度辅助爬虫](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/spiders/baidu_search_spider.py) 抓取的数据，  
	从百度搜索引擎的搜索结果页面抓取，  
	每条结果为一条记录。

* news_china

	[中国新闻网爬虫]()抓取结果，  
	以 http://sou.chinanews.com/ 为根网址。
	每个新闻页面为一条记录。

* news_qq

	[腾讯新闻网爬虫]()抓取结果，  
	借助百度搜索辅助，从 https://news.qq.com/ 抓取，
	每个新闻页面为一条记录。

* news_sina

	[新浪新闻网爬虫]()抓取结果，  
	借助百度搜索辅助，从 https://news.sina.com.cn/ 抓取，
	每个新闻页面为一条记录。

* weibo_comment

	[微博爬虫](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/spiders/weibo_spider.py) 抓取结果，  
	微博评论，每条评论为一条记录。

* weibo_infomation
	
	[微博爬虫](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/spiders/weibo_spider.py) 抓取结果，  
	微博用户个人信息，每个用户为一条记录。

* weibo_tweets

	[微博爬虫](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/spiders/weibo_spider.py) 抓取结果，  
	微博推文，每个推文为一条记录。
	
微博爬虫为了绕过桌面网页版的防爬虫机制，  
爬取的是移动网页版的微博网站。

### 1.2. DB Dictionary

#### 1.2.1 baidu_search_results

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|ObjectId|pymongo生成|5d1e9c3a33aafb07cc2ccd8d|
|`url`|String|结果网页的url|"http://www.baidu.com/link?url=大串乱码"|
|`crawl_time`|Int32|本程序爬取时间[python秒级时间戳](https://docs.python.org/2/library/time.html#time.time) |1562566660|
|`site`|String|搜索时输入的目标网站|"news.sina.com.cn"|
|`keyword`|String|搜索关键字|"中美贸易"|
|`waste`|Boolean|是否已被使用过|false|

* `url` 为百度生成url，[例](http://www.baidu.com/link?url=jd9ftem7jAMKBz10faFbEFB_DpISGCjAliyl-zUhoH0MkPwg8GVvpMu5uUoSNAR7AAxAGmztrqG2DNYryEBKnPmLoRXpTHErqYmXQA_F93u) 
	* 访问则被响应302，重定向至真正结果网址。
	* 尚不清楚该url时效，本程序爬虫设计是：  
	百度爬虫一旦完成工作，立刻执行对应爬虫，在实验中(最多千条+-)未发现失效。
	
* `crawl_time` (int(time.time()))

* `keyword` 使用绝对搜索(双引号包含搜索词，防止被分词而丢失信息)

#### 1.2.2 news collections
news_china, news_qq, news_sina

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|ObjectId|pymongo生成|5d1e9c3a33aafb07cc2ccd8d|
|`url`|String|新闻url|"https://news.qq.com/a/20160309/014618.htm"|
|`crawl_time`|Int32|本程序爬取时间[python秒级时间戳](https://docs.python.org/2/library/time.html#time.time) |1562566660|
|`keyword`|String|搜索关键字|"中美贸易"|
|`title`|String|新闻标题|"韩国国会通过中韩自贸协定 中韩贸易接近零关税"|
|`content`|String|正文内容|大段文字|
|`time`|String|发布时间|"2015-12-01-04-25-00"|
|`source`|String|发布来源|"京华时报"|
|`img`|Array|**(news_china only)** <br> 新闻图片的url的列表 |["url1","url2",...]|

* `title`,`content`,`time`,`source` 四字段受制于对应网站(随网站时间发展)不断变化的布局：  
	* 爬虫已尽可能兼容各种布局，但值仍有可能为空或无意义的内容(如空白符)。  
	* 已在爬虫端固定将字段写入(默认值为None)，因此在使用这些数据的程序中，只设计对值的判断即可。  
	（MongoDB不插入字段，记录中将连字段都不存在。）
	* 值的格式判断可使用re库，如re.compile。
	
* 有个设计失误是：  
因为现有系统没有根据发布时间搜索DB中新闻的需求，就为了方便读取把`time`字段做成string了，  
如需修改，  
需要对[ScrapySwarm.tools.time_format_util](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/tools/time_format_util.py) 的  
getCurrentTime()函数进行修改。

* 关于如何对多个表（集合）进行DB操作，参见 [我的counter程序](https://github.com/boholder/ScrapySwarm/blob/master/keyword_statistics_counter/keyword_statistics_counter.py)

#### 1.2.3 weibo_comment

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|String|微博评论id|"C_4389627255074784"|
|`weibo_url`|String|该评论的url|"https://weibo.com/2656274875/HBBoh8WVJ"|
|`crawl_time`|Int32|本程序爬取时间[python秒级时间戳](https://docs.python.org/2/library/time.html#time.time) |1562566660|
|`comment_user_id`|String|微博用户id|"2926073071"|
|`content`|String|评论正文|"..."|
|`like_num`|Int32|该评论被点赞数|150|
|`created_at`|String|评论发布时间|"2019-07-02-14-55-00"|

#### 1.2.4 weibo_infomation

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|String|微博用户id|"6740482899"|
|`head`|String|微博用户头像图片url|"http://tvax2.sinaimg.cn/crop.0.0.664.664.180(长宽+分辨率？)/随机码.jpg"|
|`crawl_time`|Int32|本程序爬取时间[python秒级时间戳](https://docs.python.org/2/library/time.html#time.time) |1562566660|
|`nick_name`|String|用户昵称|"alice"|
|`gender`|String|性别|"男"or"女"|
|`province`|String|省份or直辖市|"吉林","北京"|
|`city`|String|城市or直辖市区|"深圳","东城区"|
|`brief_introduction`|String|个人介绍|"..."|
|`vip_level`|String|用户等级|"5级"|
|`tweets_num`|Int32|发推文数|1234|
|`follows_num`|Int32|关注数|1234|
|`fans_num`|Int32|粉丝数|1234|

#### 1.2.5 weibo_tweets

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|String|微博推文id|"2286208003_H8F85wJUL"|
|`keyword`|String|搜索关键字|"中美贸易"|
|`crawl_time`|Array|本程序爬取时间[python秒级时间戳](https://docs.python.org/2/library/time.html#time.time) |[1562566660,...]|
|`weibo_url`|String|该推文的url|"https://weibo.com/2656274875/HBBoh8WVJ"|
|`user_id`|String|发推用户微博id|"6740482899"|
|`created_at`|String|推文发布时间|"2019-07-02-14-55-00"|
|`tool`|String|发布推文的工具|"人民网微博"|
|`like_num`|Array|点赞数|[100,...]|
|`repost_num`|Array|转发数|[100,...]|
|`comment_num`|Array|评论数|[100,...]|
|`image_url`|String|只取第一张推文附图的url|"http://wx2.sinaimg.cn/wap180/884f7263ly1fyhglkehyaj20c80dwabj.jpg"|
|`content`|String|推文正文|"..."|

* 注意 `crawl_time` , `like_num`, `report_num`, `comment_num` 的类型为 Array，  
需求要求对微博的同一推文每隔一段时间爬取4次，以计算趋势，故DB记录设计如此。  
当然，每项值仍为Int32类型。

* 另外有一点要注意的是，对微博推文的爬取因微博反爬虫机制，  
无法做到以推文url为目标的靶向爬取，而是借助关键字搜索，  
在结果池中爬取并识别是否已被爬过（大数量换覆盖率）。  
因此**对大多数记录来说，注意1中的四个属性的长度仅仅为1或2**。

## 2. DB: SwarmLog

### 2.1 Collections

* api_log

	[ScrapySwarm.control.swarm_api.py](https://github.com/boholder/ScrapySwarm/blob/master/ScrapySwarm/control/swarm_api.py)  
	的运行记录。

* spiders_log

	[各爬虫](https://github.com/boholder/ScrapySwarm/tree/master/ScrapySwarm/spiders) 的运行记录。  
	基本是将 [scrapy的Stats Collection](https://docs.scrapy.org/en/latest/topics/stats.html)  导出。

* keyword_statistics

	[关键字计数器程序](https://github.com/boholder/ScrapySwarm/blob/master/keyword_statistics_counter/keyword_statistics_counter.py)  所维护的，  
	关于在哪个网站爬了哪个关键字多少条数据的集合。  
	上述程序因需要不断I/O，独立从命令行运行启动，  
	不断更新该表，以实时反应爬虫的爬取情况。

### 2.2 DB Dictionary

#### 2.2.1 api_log

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|ObjectId|pymongo生成|5d1e9c3a33aafb07cc2ccd8d|
|`api_name`|String|被调用的api函数的函数名|"runOneSpider"|
|`last_modified`|Date|最后修改时间|2019-07-08T00:46:38.904+00:00|
|`start_time`|Date|开始运行时间|2019-07-08T00:46:36.651+00:00|
|`finish_time`|Date|结束运行时间|2019-07-08T00:46:38.904+00:00|
|`finish_reason`|String|结束原因(程序中判断+硬编码)|"api finished without a logfile"|
|`argsdict`|Object|调用api函数时传入的参数字典|{"keyword":"中美贸易"}|

* `argsdict` 中的键名受被调用的api函数的参数所控。

* 所有Date对象都是**UTC格式**，  
使用python的datetime.datetime.utcnow()生成。  
**下同**。

#### 2.2.2 spiders_log

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|ObjectId|pymongo生成|5d1e9c3a33aafb07cc2ccd8d|
|`spider`|String|爬虫名|"qqnews_spider"|
|`last_modified`|Date|最后修改时间|2019-07-08T00:46:38.904+00:00|
|`start_time`|Date|开始运行时间|2019-07-08T00:46:36.651+00:00|
|`finish_time`|Date|结束运行时间|2019-07-08T00:46:38.904+00:00|
|`finish_reason`|String|scrapy机制|"finished"|
|`item_scraped_count`|Int32|本次运行抓取的条数|34|
|`downloader/request_count`|Int32|爬虫向服务器请求的条数|34|
|`downloader/response_count`|Int32|服务器回复爬虫的条数|34|
|`downloader/response_bytes`|Int32|近似于抓取的数据大小|34|
|`downloader/response_status_count/{code num}`|Int32|服务器回复的各状态码的计数|34|
|`log_count/WARNING`|Int32|logger报出的warning级别的日志条数|2|
|`log_count/ERROR`|Int32|同上，error级别的日志条数|2|

* `spider` 爬虫名取scrapy爬虫的类属性 `name` ，  
但因程序设计因素，实际上name要等同于所在文件的文件(模块)名。

* `downloader/response_status_count/{code num}`   
每有一种状态码，该字段就多一个。

* `log_count/ERROR` , `log_count/WARNING`  
scrapy框架中含有调用python logging库生成的logger，  
程序员可以主动调用这些logger来添加日志，  
scrapy所属的部分的log也会向这些logger中写。  
其实5个级别的计数在scrapy的Stats Collection都有，  
但只往数据库里记录了需要注意的两个严重级别。  
（critical error要能报出来程序也爆了，也不会走到记log到DB这一步）

#### 2.2.3 keyword_statistics

|属性|类型|描述|示例|
|-|-|-|-|
|`_id`|ObjectId|pymongo生成|5d1e9c3a33aafb07cc2ccd8d|
|`keyword`|String|搜索关键字|"中美贸易"|
|`last_modified`|Date|最后修改时间|2019-07-08T00:46:38.904+00:00|
|`item_num_dict`|Object|记录**哪个表中有几条**|{"news_qq":23}|
|`old_item_num_dict`|Object|最后刷新前的记录|{"news_qq":12}|

* `item_num_dict` 示例：  
```
{
	"news_china":23,
	"news_qq":41,
	"news_sina":51,
	"weibo_comment":241,
	"weibo_infomation":0,
	"weibo_tweets":213
}
```