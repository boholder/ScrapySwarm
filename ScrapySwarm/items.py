# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class QQNewsItem(Item):
    url = Field()  # 新闻项的url
    content = Field()  # 新闻正文
    title = Field()  # 新闻标题
    time = Field()  # 新闻发布时间    format: 'YYYY-MM-DD-HH-MM-SS'
    imgs = Field()  # 新闻附属图片的url的列�
    crawl_time = Field()  # 爬虫抓取时间 format: 'YYYY-MM-DD-HH-MM-SS'
    keyword = Field()   # 搜索的关键字�exm: '中美贸易'
    source = Field()    # 新闻来源|报社


class BaiduSearchItem(Item):
    # 新闻项的url
    url = Field()
    # 本项目的baidu_search_spider抓取该url的时�
    # format: 'YYYY-MM-DD-HH-MM-SS'
    crawl_time = Field()
    # 给与 baidu_search_spider �site 参数�
    # exm:'news.qq.com'
    site = Field()
    # 搜索的关键字�exm: '中美贸易'
    keyword = Field()
    # 是否已被对应爬虫使用�(int 0 没用过| 1 用过�
    waste = Field()


class ChinaNewsItem(Item):
    """中国新闻"""
    _id=Field()  #主键，由url+time构成
    url = Field()
    content=Field()  #内容，其中保留了图片的路径，�&隔断
    title = Field()
    keyword=Field()#检索关键字
    time=Field()     #格式 YYYY-MM-DD-HH-MM-SS
    imgs=Field()     #list
    crawl_time = Field()  # 抓取时间int类型
    source=Field() #新闻来源


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()  # 微博id
    keyword = Field()  # 检索关键字
    weibo_url = Field()  # 微博URL
    created_at = Field()  # 微博发表时间
    like_num = Field()  # 点赞�
    repost_num = Field()  # 转发�
    comment_num = Field()  # 评论�
    content = Field()  # 微博内容
    user_id = Field()  # 发表该微博用户的id
    tool = Field()  # 发布微博的工�
    image_url = Field()  # 图片
    video_url = Field()  # 视频
    location = Field()  # 定位信息
    location_map_info = Field()  # 定位的经纬度信息
    origin_weibo = Field()  # 原始微博，只有转发的微博才有这个字段
    crawl_time = Field()  # 抓取时间�


class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    province = Field()  # 所在省
    city = Field()  # 所在城�
    brief_introduction = Field()  # 简�
    birthday = Field()  # 生日
    tweets_num = Field()  # 微博�
    follows_num = Field()  # 关注�
    fans_num = Field()  # 粉丝�
    sex_orientation = Field()  # 性取�
    sentiment = Field()  # 感情状况
    vip_level = Field()  # 会员等级
    authentication = Field()  # 认证
    person_url = Field()  # 首页链接
    labels = Field()  # 标签
    crawl_time = Field()  # 抓取时间�


class RelationshipsItem(Item):
    """ 用户关系，只保留与关注的关系 """
    _id = Field()
    fan_id = Field()  # 关注�即粉丝的id
    followed_id = Field()  # 被关注者的id
    crawl_time = Field()  # 抓取时间�


class CommentItem(Item):
    """
    微博评论信息
    """
    _id = Field()
    comment_user_id = Field()  # 评论用户的id
    content = Field()  # 评论的内�
    weibo_url = Field()  # 评论的微博的url
    created_at = Field()  # 评论发表时间
    like_num = Field()  # 点赞�
    crawl_time = Field()
