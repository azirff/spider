#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-10-07 13:22:56
# Project: bosspyspider
from pyspider.libs.base_handler import *
import pymysql
import MySQLdb
import time
from datetime import datetime
import requests
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

etree = lxml.html.etree


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'Host': "www.zhipin.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)  Gecko/20100101     Firefox/69.0',
            'Accept': 'text/css,*/*;q=0.1',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    }

    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', '123456', 'xx', charset='utf8')
        #初始化数据库

    def add_Mysql(self, title):
        #定义将数据插入数据库的方法
        try:
            cursor = self.db.cursor()
            sql = 'insert into workss(title) values ("%s")' % (title);  # 插入数据库的SQL语句
            print(sql)
            cursor.execute(sql)
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def cook(self):
        #定义cookies获取的方法
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        browser = webdriver.Chrome(options=options)
        wait = WebDriverWait(browser, 10)  # 超时时长为10s
        browser.get(
            'https://www.zhipin.com/job_detail/?query=%E7%89%A9%E8%81%94%E7%BD%91&city=101010100&industry=&position=')
        time.sleep(2)
        global cookies
        cookies = {}
        c = browser.get_cookies()
        for cookie in c:
            cookies[cookie['name']] = cookie['value']

    @every(minutes=24 * 60)
    def on_start(self):
        #pyspider入口
        self.cook()
        print(cookies)
        self.crawl(
            'https://www.zhipin.com/job_detail/?query=%E7%89%A9%E8%81%94%E7%BD%91&city=101010100&industry=&position=',
            callback=self.index_page, cookies=cookies, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #定义数据页链接采集方法
        self.cook()
        print(cookies)
        i = 1
        for each in response.doc(
                '.job-list > ul > li > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)').items():
            if i % 3 == 0:
                self.cook()
            self.crawl(each.attr.href, callback=self.detail_page, cookies=cookies, validate_cert=False)
            #将数据页链接传递给detail_page（）方法
            i = i + 1
        #每请求3次重新获取一次cookie
        next = response.doc('.next').attr.href
        self.crawl(next, callback=self.index_page, cookies=cookies, validate_cert=False)
        #爬取到下一页的链接再次回传给index_page（）方法

    @config(priority=2)
    def detail_page(self, response):
        #解析链接并定义数据的采集方法
        title = response.doc('.job-primary > div:nth-child(2) > div:nth-child(2) > h1:nth-child(1)').text()
        print(title)
        self.add_Mysql(title)
        return {
            "title": response.doc('.job-primary > div:nth-child(2) > div:nth-child(2) > h1:nth-child(1)').text(),
        }