# SracpySwarm.CenterControl Subsystem Idea

**2019-06-25 by boholder**

## 0.db-access  (DB query & insert [& delete, update])

数据库操作模块，因为数据库还没敲定是mongodb还是mysql，  
所以暂时只写几个桩函数，返回boolean。

这个模块有几个函数要看剩下的，随机应变，先不设计。

## 1.log-util (called by spiders & run-control to send log to DB)

这个也暂时没法设计，要借助scrapy提供的API，还没读文档。  
或者要自己写一些主控层面的，爬虫运行记录。

## 2.run-control (run spiders by cmdline.execute())

* runSpider(spider, keyword, Timer=None)
	* @param `spider`  \{string\} 爬虫名(name)
	* @param`keyword `\{string\} 关键字 
	* @param`Timer`  \{Timer\} 定时器
	* @return Synchronize? Asynchronous?What?
* Timer(second, repeatnum=1)
	* @param`second `\{int\} 间隔秒数
	* @param`repeatnum` \{int\} 重复次数 ，默认只运行一次
	* 3组说要对同一微博每隔多久爬取一次评论与点赞数  
	这个功能的使用应该与数据库表设计和爬虫实现结合。
* runAllSpiders(keyword)
	* @param`keyword `\{string\} 关键字 
	* @return What?
## 3.cc-api (called by upper system to run spiders | view log)

算是一个接口模块，接受其他上层系统的调用，  
查询DB|执行爬虫，并返回可供做决定的返回值  
（指boolean和log信息字典）。

暂时不设计，应该是把上面其他模块的函数都抽象出  
一个接口函数就行了，也可能有些简化控制方面的封装逻辑。  
比如runAllSpiders() 也可以做在这一个模块。