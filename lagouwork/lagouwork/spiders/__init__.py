import random

import pandas
import pymysql
import scrapy
from ..items import LagouworkItem
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
import json
etree=lxml.html.etree
from bs4 import BeautifulSoup
agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",]
headers = {
    'User-Agent': random.choice(agents),
    'Referer': 'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
    'Host': 'www.lagou.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
cursor = db.cursor()
sql = 'select *from lagouwork;'
c = pandas.read_sql(sql, db)
db.close()
class lagoupider(scrapy.Spider):
    name='lagou'

    def start_requests(self):
        formdata = {
            'first': 'true',
            'pn': '1',
            'kd': '物联网'
        }
        resp = requests.get(
            'https://www.lagou.com/jobs/allCity.html?keyword=%E7%89%A9%E8%81%94%E7%BD%91&px=default&city=%E5%85%A8%E5%9B%BD&positionNum=127&companyNum=0&isCompanySelected=false&labelWords',
            headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        vie = soup.select('#main_container > div > div.cityContainer > table.word_list > tr >td>ul.city_list >li>a ')
        #先爬取所有城市后依次发出请求
        for i in vie:
            yield scrapy.FormRequest('https://www.lagou.com/jobs/positionAjax.json?hy=%E5%85%B6%E4%BB%96&px=default&city={}&needAddtionalResult=false'.format(i.text),dont_filter=True,headers=headers,formdata=formdata,callback=self.parse,meta={'pn':1,'dont_redirect': True,
                'handle_httpstatus_list': [302]})
        #使url不会被过滤，不会被重定向，并将页数值传递下去
    def parse(self,response):
        jd = json.loads(response.text)
        # 将str数据转换成字典类型
        js = jd['content']['positionResult']['result']
        # 获取字典中到所有数据存入js列表中
        cc = []
        for xx in js:
            # 通过for遍历得到该页所有工作链接值
            cc.append(xx['positionId'])
        if cc == []:
            #若数据返回为空则该城市爬完所有页
            print('爬完所有页')
        else:
            init_url = response.url
            q = response.meta['pn']
            q = q + 1
            s = str(q)
            # 增加页数值
            formdata = {
                'first': 'true',
                'pn': s,
                'kd': '物联网'
            }
            yield scrapy.FormRequest(init_url, formdata=formdata, headers=headers, callback=self.parse, meta={'pn': q,'dont_redirect': True,
                'handle_httpstatus_list': [302]},dont_filter=True)
            #使url不会被过滤，不会被重定向，并将页数值传递下去
            for o in cc:
                o=str(o)
                url='https://www.lagou.com/jobs/'+o+'.html'
                #合成工作页链接
                xx=url in c["url"].values
                if xx ==False:
                #如果链接不在一爬取的数据中则发出请求
                    yield scrapy.Request(url,dont_filter=True,headers=headers,callback=self.parse_job,meta={'o':o,'dont_redirect': True,
                'handle_httpstatus_list': [302]})
                # 使url不会被过滤，不会被重定向，并将页数值传递下去
            print('正爬取第' + s + '页')

    def parse_job(self,response):
        #处理返回的数据存入item
        try:
            industry = response.xpath('//ul[@class="c_feature"]/li/i[@class="icon-glyph-fourSquare"]/../h4/text()')[0].extract()
        except:industry=''
        try:
            company = response.xpath('//dl[@class="job_company"]/dt/a/img/@alt')[0].extract()
        except:company=''
        try:
            size = response.xpath('//ul[@class="c_feature"]/li/i[@class="icon-glyph-figure"]/../h4/text()')[0].extract()
        except:size=''
        try:
            financing = response.xpath('//ul[@class="c_feature"]/li/i[@class="icon-glyph-trend"]/../h4/text()')[0].extract()
        except:financing=''
        try:
            city = response.xpath('//dd[@class="job_request"]/h3/span[2]/text()')[0].extract()
        except:city = ''
        try:
            experience = response.xpath('//dd[@class="job_request"]/h3/span[3]/text()')[0].extract()
        except:experience=''
        try:
            education = response.xpath('//dd[@class="job_request"]/h3/span[4]/text()')[0].extract()
        except:education=''
        try:
            work = response.xpath('//div[@class="position-head"]/div/div/div/h1[@class="name"]/text()')[0].extract()
        except:work = ''
        try:
            wages = response.xpath('//dd[@class="job_request"]/h3/span[1]/text()')[0].extract()
        except:wages=''
        try:
            url = response.url
        except:url=''
        try:
            welfare = response.xpath('//dd[@class="job-advantage"]/p/text()')[0].extract()
        except:welfare=''
        try:
            conditions = response.xpath('//dd[@class="job_bt"]/div[@class="job-detail"]/p/text()')[0:].extract()
        except:conditions=''
        item = LagouworkItem()
        item['industry'] = industry
        item['company'] = company
        item['size'] = size
        item['financing'] = financing
        item['city'] = city
        item['experience'] = experience
        item['education'] = education
        item['work'] = work
        item['wages'] = wages
        item['url'] = url
        item['welfare'] = welfare
        item['conditions'] = conditions
        yield item