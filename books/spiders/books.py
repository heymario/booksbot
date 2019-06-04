# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
import time

class ArticleItem(scrapy.item.Item):
    title = scrapy.Field(alias='标题', required=True)
    danwei = scrapy.Field(alias='单位')
    date = scrapy.Field(alias='日期')
    url = scrapy.Field(alias='链接')
    

class bidSpider(scrapy.Spider):
    name = "bid"
    def start_requests(self):
        for i in range(1,2000):
            page_url = 'http://www.bidding.csg.cn/zbcg/index_%d.jhtml' %(i)
            yield scrapy.Request(url=page_url, callback=self.parse_article)

#    def parse_list(self, response):
#        for i in range(1,2):
#            page_url = 'http://www.bidding.csg.cn/zbcg/index_%d.jhtml' %(i)
#            yield scrapy.Request(url=page_url, callback=self.parse_article)
    def parse_article(self, response):
        selector = scrapy.Selector(response)
        article = ArticleItem()
        danwei = selector.xpath("//div[@class='BorderEEE NoBorderTop List1 Black14 Padding5']/ul/li/text()").extract()
        title = selector.xpath("//div[@class='BorderEEE NoBorderTop List1 Black14 Padding5']/ul/li/a/@title").extract()
        date = selector.xpath("//div[@class='BorderEEE NoBorderTop List1 Black14 Padding5']/ul/li/span/text()").extract()
        url = selector.xpath("//div[@class='BorderEEE NoBorderTop List1 Black14 Padding5']/ul/li/a/@href").extract()
        for a,b,c,d in zip(danwei, title, date, url):
            article['danwei'] = a
            article['title'] = b
            article['date'] = c
            article['url'] ='http://www.bidding.csg.cn' + d
            yield article
