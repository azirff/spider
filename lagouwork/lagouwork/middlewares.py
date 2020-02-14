# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
from fnmatch import fnmatch

import pandas
import pymysql
from scrapy import signals


class LagouworkSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouworkDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
import random
import scrapy

import requests
import time
# logger = logging.getLogger()
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import FirefoxOptions
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import lxml.html
import json
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
ConnectionRefusedError, ConnectionDone, ConnectError, \
ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
etree=lxml.html.etree
ipurl='https://too.ueuz.com/frontapi/public/http/get_ip/index?type=-1&iptimelong=9&ipcount=1&protocol=0&areatype=2&area=440000&resulttype=txt&duplicate=0&separator=1&other=&show_city=0&show_carrier=0&show_expire=0&isp=-1&auth_key=3de056f4ba7e09b0f30dc0cc07e09638&app_key=acd2b3f6d6af88f27c42b2559e00ab61&timestamp=1574411517&sign=51BD34F5108671AE14C83681779615EC'
class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    def head(self,proxies):
        # 获取cookies
        cc={}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Referer': 'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
            'Host': 'www.lagou.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        resp = requests.get(
            'https://www.lagou.com/jobs/list_%E7%89%A9%E8%81%94%E7%BD%91?labelWords=&fromSearch=true&suginput=',
            allow_redirects=False,proxies=proxies,
            headers=headers, timeout=10, verify=False)
        cc = resp.cookies.get_dict()
        return cc
        # 返回cookies
    def givep(self):
        #随机去一个ip
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
        cursor = db.cursor()
        sql = 'select *from p;'
        c = pandas.read_sql(sql, db)
        if c.shape[0] < 2:
        #ip总数小于2就补充
            print('123')
            os.system('python D:/spider/lagouwork/lagouwork/pool.py')
            db.close()
            db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
            cursor = db.cursor()
            c= pandas.read_sql(sql, db)
        s = c.sample()
        db.close()
        return s
    def p(self,s):
        #判断ip是否过期
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
        cursor = db.cursor()
        while True:
            proxies = {'https': '{}'.format(s.loc[s.index[0],'p'])}
            try:
                requests.get('https://www.baidu.com', timeout=8, proxies=proxies)
                break
            except:
                sql = 'delete from p where p="%s";' % (s.loc[s.index[0],'p'])
                if cursor.execute(sql):
                        db.commit()
                        sql = 'select *from p;'
                        c = pandas.read_sql(sql, db)
                        if c.shape[0] < 2:
                            db.close()
                            print('ip储存小于2')
                            os.system('python D:/pycharm/py/lagouwork/lagouwork/pool.py')
                            print('已经添加好ip')
                            db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
                            cursor = db.cursor()
                        q = pandas.read_sql(sql, db)
                        print(q)
                        s = q.sample()
                        print("S")
        db.close()
        return s
    def c(self,s):
        #使用取到的ip获取cookies
        proxies = {'https': '{}'.format(s.loc[s.index[0],'p'])}
        data = self.head(proxies)
        return data
    def process_request(self, request, spider):
        a=self.givep()
        # 随机去一个ip
        b=self.p(a)
        # 判断ip是否过期
        c=self.c(b)
        # 使用取到的ip获取cookies
        print(c)
        request.cookies = c
        request.meta['proxy'] = 'http://' + b.loc[b.index[0],'p']
        return None
    def process_response(self, request, response, spider):
        if response.status==302:
            return request
        return response
    def  process_exception(self,request, exception,spider):
        if isinstance( exception,TimeoutError):

            return request