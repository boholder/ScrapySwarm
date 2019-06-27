#!/usr/bin/python3

# encoding: utf-8
import os
import re
from lxml import etree
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

from ScrapySwarm.items import TweetsItem, \
    CommentItem, RelationshipsItem, InformationItem
from ScrapySwarm.tools.weibo_utils import time_fix, \
    extract_weibo_content, extract_comment_content
import time

class WeiboSpider(Spider):
    name = "weibo_spider"
    hotbase_url = "https://weibo.cn/search/mblog?" \
               "hideSearchFrame=&keyword=#" \
               "&advancedfilter=1&sort=hot&page="
    base_url = "https://weibo.cn/search/mblog?" \
               "keyword=#" \
               "&sort=time&page="
    custom_settings = {
        # 请将Cookie替换成你自己的Cookie
        'DOWNLOAD_DELAY' : 5,
        'COOKIES_ENABLED':False,
        'DEFAULT_REQUEST_HEADERS' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie':'_T_WM=f7fc1975334e2610dd77c4a949caaa2e; __guid=78840338.2690867225963806000.1561098303'
                     '394.3926; TMPTOKEN=xWotEi1ho4BsQadI1WKh50PW3wxeD0MXriFaU01sHfs7ddDfYkc6g8QC0brRQ2iI; SUB=_2A25'
                     'wCAggDeRhGeBM6lER8yzJzD2IHXVT8qhorDV6PUJbkdAKLUnFkW1NRRuUuWjxLqOlReVo19AJKlLVFf0K-Qcb; SUHB=0h1J3'
                     'h4MnoA8ye; SCF=AqNspA5hvpJAB-QOIpSEFOvS7uTz2C-xcjU2d4im-izONxHBJbLovO6aDcPk7st0qIDcNhWWOxTPgrhwE'
                     'NoLpoA.; SSOLoginState=1561098352; monitor_count=2'
        }
    }

    q = []

    def start_requests(self):
        querystr = getattr(self, 'q', '中美贸易')
        self.querystr=querystr
        folderpath = "e:\weibo" +querystr
        if (not os.path.exists(folderpath)):
            os.mkdir(folderpath)
        folderpath = "e:\weibo"
        if (not os.path.exists(folderpath)):
            os.mkdir(folderpath)


        self.q=[]
        self.base_url=self.base_url.replace("#",querystr)
        self.hotbase_url = self.hotbase_url.replace("#", querystr)
        yield Request(url=self.hotbase_url+"1", callback=self.parse_tweet)
        # yield Request(url=self.base_url + "1", callback=self.parse_tweet)



    def parse_url(self,response):
        print('我被调用了哦')
        if  response.url.endswith('page=1'):
            # 如果是第1页，一次性获取后面的所有页
            all_page = re.search(r'&nbsp;1/(\d+)页', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                print('获取到了页数',all_page)
                if all_page>=99:
                    all_page=220
                for page_num in range(2,all_page):
                    page_url = response.url.replace(
                        'page=1', 'page={}'.format(page_num))
                    yield Request(url=page_url, callback=self.parse_url,
                                  dont_filter=True, meta=response.meta)
        """
        解析本页的数据
        """
        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
                tweet_repost_url = tweet_node.xpath(
                    './/a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(
                    r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                weibo_url = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),user_tweet_id.group(1))
                yield Request(url=weibo_url,callback= self.parse_details,
                              dont_filter=True, meta=response.meta,args={'wait': 2})

    def parse_details(self,response):
        body = response.body
        body = body.decode("utf-8")
        # print(body)
        selector =Selector(text=body)
        headandname = selector.xpath('//div[@class="face"]/a[@class="W_face_radius"]')[0]
        head=headandname.xpath("./img/@src").get()
        author_name=headandname.xpath("./@title").get()
        author_url=headandname.xpath("./@href").get()

        timeandfrom=selector.xpath('//div[@class="WB_from S_txt2"]')[0]
        posttime=timeandfrom.xpath("./a")[0].xpath("./@title").get()
        timeArray = time.strptime(posttime, "%Y-%m-%d %H:%M")
        created_at =time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
        crawl_time= str(int(time.time()))
        tool=""
        if len(timeandfrom.xpath("./a"))>1:
            tool=timeandfrom.xpath("./a")[1].xpath("./text()").get()

        content1 =selector.xpath('//div[@class="WB_text W_f14"]')
        content =content1.get()
        p = re.sub(r'<.*?>', '', content)
        content = re.sub(r'  ', '', p).strip()
        location1=''
        location1 =content1.xpath('./a/i[@class="W_ficon ficon_cd_place"]')
        if location1:
            location=location1.xpath('../@title').get()
            content=content.rstirp(location)
            print(content,location)









    def parse_information(self, response):
        """ 抓取个人信息 """
        information_item = InformationItem()
        information_item['crawl_time'] = int(time.time())
        selector = Selector(response)
        information_item['_id'] = re.findall('(\d+)/info', response.url)[0]

        # 获取标签里的所有text()
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;?[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        labels = re.findall('标签;?[：:]?(.*?)更多>>', text1)
        if nick_name and nick_name[0]:
            information_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            information_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            information_item["province"] = place[0]
            if len(place) > 1:
                information_item["city"] = place[1]
        if briefIntroduction and briefIntroduction[0]:
            information_item["brief_introduction"] = \
                briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            information_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                information_item["sex_orientation"] = "同性恋"
            else:
                information_item["sex_orientation"] = "异性恋"
        if sentiment and sentiment[0]:
            information_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vip_level and vip_level[0]:
            information_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            information_item["authentication"] = authentication[0].replace(u"\xa0", "")
        if labels and labels[0]:
            information_item["labels"] = \
                labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        request_meta = response.meta
        request_meta['item'] = information_item
        yield Request(self.base_url + '/u/{}'.format(information_item['_id']),
                      callback=self.parse_further_information,
                      meta=request_meta, dont_filter=True, priority=1)

    def parse_further_information(self, response):
        text = response.text
        information_item = response.meta['item']
        tweets_num = re.findall('微博\[(\d+)\]', text)
        if tweets_num:
            information_item['tweets_num'] = int(tweets_num[0])
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            information_item['follows_num'] = int(follows_num[0])
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            information_item['fans_num'] = int(fans_num[0])
        yield information_item

        # 获取该用户微博
        yield Request(url=self.base_url +
                          '/{}/profile?page=1'.format(information_item['_id']),
                      callback=self.parse_tweet,
                      priority=1)

        # 获取关注列表
        yield Request(url=self.base_url +
                          '/{}/follow?page=1'.format(information_item['_id']),
                      callback=self.parse_follow,
                      dont_filter=True)
        # 获取粉丝列表
        yield Request(url=self.base_url +
                          '/{}/fans?page=1'.format(information_item['_id']),
                      callback=self.parse_fans,
                      dont_filter=True)


    def parse_tweet(self, response):
        body = response.body
        body = body.decode("utf-8")
        print(body)
        # if  response.url.endswith('page=1'):
        #     # 如果是第1页，一次性获取后面的所有页
        #     all_page = re.search(r'&nbsp;1/(\d+)页', response.text)
        #     if all_page:
        #
        #         all_page = all_page.group(1)
        #         all_page = int(all_page)
        #         print('获取到了页数',all_page)
        #         if all_page>=99:
        #             all_page=220
        #         for page_num in range(2,93):
        #             page_url = response.url.replace(
        #                 'page=1', 'page={}'.format(page_num))
        #             yield Request(page_url, self.parse_tweet,
        #                           dont_filter=True, meta=response.meta)
        """
        解析本页的数据
        """
        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetsItem()
                tweet_item['keyword']=self.querystr
                tweet_item['crawl_time'] =[]
                tweet_item['crawl_time'].append(str(int(time.time())))
                tweet_repost_url = tweet_node.xpath(
                    './/a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(
                    r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['weibo_url'] = \
                    'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),
                                                    user_tweet_id.group(1))
                tweet_item['user_id'] = user_tweet_id.group(2)
                tweet_item['_id'] = '{}_{}'.format(user_tweet_id.group(2),
                                                   user_tweet_id.group(1))
                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:
                    tweet_item['created_at'] = \
                        time_fix(create_time_info.split('来自')[0].strip())
                    tweet_item['tool'] = create_time_info.split('来自')[1].strip()
                else:
                    tweet_item['created_at'] = time_fix(create_time_info.strip())

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                tweet_item['like_num'] = []
                tweet_item['like_num'].append( int(re.search('\d+', like_num).group()))
                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                tweet_item['repost_num'] = []
                tweet_item['repost_num'].append(int(re.search('\d+', repost_num).group()))
                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") '
                    'and not(contains(text(),"原文"))]/text()')[-1]
                tweet_item['comment_num'] = []
                tweet_item['comment_num'].append(int(re.search('\d+', comment_num).group()))
                images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                if images:
                    tweet_item['image_url'] = images[0]

                videos = tweet_node.xpath('.//a[contains(@href,'
                                          '"https://m.weibo.cn/s/video/show?object_id=")]'
                                          '/@href')
                if videos:
                    tweet_item['video_url'] = videos[0]

                map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                if map_node:
                    map_node = map_node[0]
                    map_node_url = map_node.xpath('./@href')[0]
                    map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                    tweet_item['location_map_info'] = map_info
                    tweet_item['location'] = \
                        map_node.xpath('./preceding-sibling::a/text()')[0]

                repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                if repost_node:
                    tweet_item['origin_weibo'] = repost_node[0]

                # 检测由没有阅读全文:
                # all_content_link =
                #   tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                # if all_content_link:
                #     all_content_url =
                #       self.base_url + all_content_link[0].xpath('./@href')[0]
                #     yield Request(all_content_url,
                #                   callback=self.parse_all_content,
                #                   meta={'item': tweet_item},
                #                   priority=1)
                #
                # else:
                tweet_html = etree.tostring(tweet_node, encoding='unicode')
                tweet_item['content'] = extract_weibo_content(tweet_html)
                if not tweet_item['_id'] in self.q:
                    self.q.append(tweet_item['_id'])
                    yield tweet_item

                # 抓取该微博的评论信息
                comment_url = 'https://weibo.cn/comment/hot/' \
                              + tweet_item['weibo_url'].split('/')[-1] + '?rl=2'
                print(comment_url)
                yield Request(url=comment_url,
                              callback=self.parse_comment,
                              meta={'weibo_url': tweet_item['weibo_url']})

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        # 有阅读全文的情况，获取全文
        body = response.body

        body = body.decode("utf-8", "ignore")
        # print(body)
        # print(body)
        response.replace(body=body)
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html)
        self.q.append(tweet_item[''])
        yield tweet_item

    def parse_follow(self, response):
        """
        抓取关注列表
        """
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_follow,
                                  dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" '
                              'or text()="取消关注"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/follow', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item['crawl_time'] = int(time.time())
            relationships_item["fan_id"] = ID
            relationships_item["followed_id"] = uid
            relationships_item["_id"] = ID + '-' + uid
            yield relationships_item

    def parse_fans(self, response):
        """
        抓取粉丝列表
        """
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_fans,
                                  dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" '
                              'or text()="移除"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/fans', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item['crawl_time'] = int(time.time())
            relationships_item["fan_id"] = uid
            relationships_item["followed_id"] = ID
            relationships_item["_id"] = uid + '-' + ID
            yield relationships_item

    def parse_comment(self, response):
        # 如果是第1页，一次性获取后面的所有页
        # if response.url.endswith('page=1'):
        #     all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
        #     if all_page:
        #         all_page = all_page.group(1)
        #         all_page = int(all_page)
        #         for page_num in range(2, all_page + 1):
        #             page_url = response.url.replace('page=1', 'page={}'.format(page_num))
        #             yield Request(page_url, self.parse_comment,
        #                           dont_filter=True, meta=response.meta)
        body = response.body

        body = body.decode("utf-8")
        # print(body)
        # print(body)
        response.replace(body=body)
        print(response.body)
        tree_node = etree.HTML(response.body)
        comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = int(time.time())
            comment_item['weibo_url'] = response.meta['weibo_url']
            comment_item['comment_user_id'] = \
                re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
            comment_item['content'] = \
                extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
            comment_item['_id'] = comment_node.xpath('./@id')[0]
            created_at_info = comment_node.xpath('.//span[@class="ct"]/text()')[0]
            like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            comment_item['like_num'] = int(re.search('\d+', like_num).group())
            comment_item['created_at'] = time_fix(created_at_info.split('\xa0')[0])
            people_url='https://weibo.cn/u/'+comment_item['comment_user_id']
            yield Request(people_url, self.parse_head,
                                      dont_filter=True, meta=comment_item)

    def parse_head(self, response):
        body = response.body

        body = body.decode("utf-8")
        selector = Selector(text=body)
        head_url=selector.xpath('//img[@alt="头像"]//@src').get()
        item =response.meta
        item['head_url']=head_url
        print(type(item),item)
        yield  item



if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('weibo_spider')
    process.start()
