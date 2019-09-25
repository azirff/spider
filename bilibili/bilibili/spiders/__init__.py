import scrapy
from ..items import BilibiliItem

class bilibilispider(scrapy.Spider):
#创建爬虫spider类
    name='bilibili'
    #定义爬虫唯一名
    allowed_domains=["bilibili.com"]
    #定义域名
    start_urls=['https://api.bilibili.com/x/v1/dm/list.so?oid=118495053']
    #定义爬取的链接
    def parse(self,response):
    #定义response的解析提取方法
        for line in response.xpath('/i/d/text()').extract():
        #遍历每一条提取的弹幕，依次存入item
            item = BilibiliItem()
            item['danmu']=line
            yield  item