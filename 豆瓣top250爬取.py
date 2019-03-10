import time
from datetime import datetime
from os.path import join
import sqlite3
import pandas
import lxml.html
etree=lxml.html.etree
import os
import requests
etree=lxml.html.etree
import json
import os
import requests
from bs4 import BeautifulSoup
def cc(newurl):
    res=requests.get(newurl,headers=header,verify=False)
    #使用requests访问newurl，添加verify=False是因为我的requests版本过高有的网页无法
    #访问
    respond = etree.HTML(res.text)
    hr=respond.xpath('//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/@href')
    #解析网页并获取到该页中的所有链接
    return hr
    #放回所有链接
def vv(href):
        result={}
        #定义字典
        dd=requests.get(href,headers=header,verify=False)
        ss=etree.HTML(dd.text)
        name=ss.xpath('//div[@id="wrapper"]/div[@id="content"]/h1/span/text()')[0]
        director=ss.xpath('//div[@id="info"]/span/span[@class="attrs"]/a/text()')[0]
        score=ss.xpath('//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]/div[@class="rating_self clearfix"]/strong/text()')[0]
        comment=ss.xpath('//div[@class="rating_right "]/div[@class="rating_sum"]/a/span/text()')[0]
        result['title']=name
        result['director']=director
        result['score']=score
        result['comment']=comment
        #取得所有内容并添加到字典
        return result
if __name__ == '__main__':
    url = 'https://movie.douban.com/top250?start={}&filter='
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Cookie': 'bid=2vOrxTfUIsI; ll="118316"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1552117732%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DiQInU_nJntejzNpCkarmTT8pRAYsUOCmEBXWBlbVNsc6ZeBdk4dcJCjVLm_eIrpb%26wd%3D%26eqid%3Df33a158c0005cceb000000065c83613d%22%5D; _pk_id.100001.4cf6=9d61672678848d14.1525601320.14.1552118604.1552115422.; __yadk_uid=xaowxBV1WqXFJsEFzMVFNvEkadYC9Gph; _vwo_uuid_v2=D6ACB1A7228ECEC8FC4E06407C39B582B|9fd5f1ec7ef6a09e5defd447bd2b1818; __utma=30149280.1516199695.1536979752.1552113986.1552117733.15; __utmz=30149280.1552117733.15.14.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1849740490.1536979752.1552113986.1552117733.13; __utmz=223695111.1552117733.13.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19215; dbcl2="193075603:ao1RGhRb6A8"; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; ck=2llh; ps=y; _pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1552117733; __utmb=223695111.6.10.1552117733; __utmt=1'
    }
    #设置浏览器的头部信息，把requests请求伪装出浏览器行为并且添加cookie实现cookie登陆，
    #在爬取豆瓣top250时第一遍爬成功时第二遍就会让你登陆，这里只需要添加cookie就能够登陆
    #当然除了登陆，你也可以设置time.sleep（）来控制
    i = 0
    #设置翻页
    a= 1
    #记录爬取页数
    movie_total=[]
    #设置列表用于添加所有链接返回的数据
    while True:
        newurl = url.format(i)
        print('正在爬取第'+str(a)+'页')
        hr=cc(newurl)
        #将newurl传到cc方法中并调用得到的返回值赋给hr
        print(hr)
        for href in hr:
            movie_total.append(vv(href))
        #通过for循环将hr中一页的所有链接赋给href，再通过for循环能够遍历所有hr元素
        #在调用vv方法就能得到数据，通过.append方法添加到列表后面
        i = 25 + i
        a= a+1
        time.sleep(3)
        if i == 250:
            break
        #当i=250时就爬到了所有数据就可以通过break退出循环
    df=pandas.DataFrame(movie_total)
    #最后通过pandas整理数据
    print(df)
