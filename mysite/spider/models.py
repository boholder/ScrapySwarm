import datetime
import json

from django.db import models

# Create your models here.

import mongoengine

class keyword_statistics (mongoengine.Document):

    _id=mongoengine.StringField()
    keyword=mongoengine.StringField(max_length=16)
    item_num_dict = mongoengine.DictField()
    old_item_num_dict= mongoengine.DictField()
    last_modified=mongoengine.StringField()


    # def default(self, obj):
    #     if isinstance(obj, datetime):
    #         return obj.__str__()
    #     return json.JSONEncoder.default(self, obj)


    def sum(self):
        s= 0
        for q in self.item_num_dict:
            s=s+int(self.item_num_dict[q])
        return s

    def __str__(self):

        datadict = {}
        datadict['news_china'] = "中国新闻网"
        datadict['news_sina'] = "新浪新闻"
        datadict['news_qq'] = "腾讯新闻"
        datadict['weibo_tweets'] = "微博"
        datadict['weibo_comment'] = "微博评论"
        datadict['weibo_infomation'] = "微博用户"

        items=str(self.item_num_dict)
        for i in datadict:
            items=items.replace(i,datadict[i])
        return "关键字:"+self.keyword+";数目:"+items

