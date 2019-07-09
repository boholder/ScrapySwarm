# Set Up Environment For ScrapySwarm
# 环境搭建

* 本程序需要以下python库：
	* Scrapy 1.6.0+ 
		* pip install Scrapy
	* pymongo 3.8.0+ 
		* 因使用了[db.collection.count_documents()](https://docs.mongodb.com/manual/reference/method/db.collection.countDocuments/)方法，需新版pymongo
		* pip install pymongo
	
* 需要自行安装 [MongoDB](https://www.mongodb.com/)

* 需要在MongoDB中提前建立两个数据库：
	* WebData
	* SwarmLog
	
* 需要使ScrapySwarm可识别
	* 1.将路径加入系统变量(以使其被作为库看待)
	* 如不可识别，将报 ModuleNotFoundError 错
	* 2.或用绝对引用相对引用等方法，只要保证识别就好