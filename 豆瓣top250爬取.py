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
    respond = etree.HTML(res.text)
    hr=respond.xpath('//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/@href')
    return hr
def vv(href):
        result={}
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
        return result
if __name__ == '__main__':
    url = 'https://movie.douban.com/top250?start={}&filter='
    header={
        'Cookie': 'bid=2vOrxTfUIsI; ll="118316"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1552117732%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DiQInU_nJntejzNpCkarmTT8pRAYsUOCmEBXWBlbVNsc6ZeBdk4dcJCjVLm_eIrpb%26wd%3D%26eqid%3Df33a158c0005cceb000000065c83613d%22%5D; _pk_id.100001.4cf6=9d61672678848d14.1525601320.14.1552118604.1552115422.; __yadk_uid=xaowxBV1WqXFJsEFzMVFNvEkadYC9Gph; _vwo_uuid_v2=D6ACB1A7228ECEC8FC4E06407C39B582B|9fd5f1ec7ef6a09e5defd447bd2b1818; __utma=30149280.1516199695.1536979752.1552113986.1552117733.15; __utmz=30149280.1552117733.15.14.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1849740490.1536979752.1552113986.1552117733.13; __utmz=223695111.1552117733.13.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19215; dbcl2="193075603:ao1RGhRb6A8"; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; ck=2llh; ps=y; _pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1552117733; __utmb=223695111.6.10.1552117733; __utmt=1'
    }
    i = 0
    a= 1
    movie_total=[]
    while True:
        newurl = url.format(i)
        print('正在爬取第'+str(a)+'页')
        hr=cc(newurl)
        print(hr)
        for href in hr:
            movie_total.append(vv(href))
        i = 25 + i
        a= a+1
        time.sleep(3)
        if i == 250:
            break
    df=pandas.DataFrame(movie_total)
    print(df)
