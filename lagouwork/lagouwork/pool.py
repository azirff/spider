import sqlite3
import time

import pandas
import pymysql
import requests
import json
from bs4 import BeautifulSoup
import urllib3

#配置代理IP池
def write(proxy):
    db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
    cursor = db.cursor()
    sql = 'insert into p(p) values("%s");' % (proxy)
    try:
        if cursor.execute(sql):
            print("Successful")
            db.commit()
    except:
        print("Failed........")
        db.rollback()
    db.close()
if __name__ == '__main__':
    ipurl='https://too.ueuz.com/frontapi/public/http/get_ip/index?type=-1&iptimelong=20190813&ipcount=3&protocol=0&areatype=1&area=&resulttype=txt&duplicate=0&separator=1&other=&show_city=0&show_carrier=0&show_expire=0&isp=-1&auth_key=3de056f4ba7e09b0f30dc0cc07e09638&app_key=acd2b3f6d6af88f27c42b2559e00ab61&timestamp=1581316411&sign=780B4CBD7D2D7D52341BB25D30077123'
    while True:
        try:
            cc = requests.get(ipurl,timeout=10)
            break
        except:print('超时')
    proxy = cc.text
    c = proxy.split('\r\n')
    c=[i for i in c if i !='']
    for p in c:
        proxies = {'https': '{}'.format(p)}
        try:
            requests.get('https://www.baidu.com/baidu?wd=123&tn=monline_4_dg&ie=utf-8',timeout=8, proxies=proxies)
            write(p)
        except:print("ip过期")

