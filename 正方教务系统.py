import urllib
from io import BytesIO
from os.path import join
import sqlite3
import xlsxwriter
import xlwt
import pandas
import lxml.html
from PIL import Image

etree = lxml.html.etree
import json
import os
import requests
from bs4 import BeautifulSoup


def ff():
    user = input('请输入学号：')
    password = input('请输入密码：')
    header = {
        'Host': '210.37.0.22',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Referer': 'http://www.hainnu.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    s = requests.session()
    ur = 'http://210.37.0.22/'
    qq = s.get(ur, headers=header)
    ss = s.cookies
    soup = BeautifulSoup(qq.text, 'html.parser')
    vie = soup.select('input[name="__VIEWSTATE"]')[0]['value']
    res = s.get('http://210.37.0.22/CheckCode.aspx', headers=header, cookies=ss)
    img = Image.open(BytesIO(res.content))
    img.show()
    txtSecretCode = input('请输入验证码:')
    print('ggggggggggggggggggggggggggggggg')
    paem = {
        'txtUserName': user,
        'TextBox2': password,
        'txtSecretCode': txtSecretCode,
        'RadioButtonList1': '学生',
        '__VIEWSTATE': vie,
        'Textbox1': '',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': '',
    }
    dat = urllib.parse.urlencode(paem).encode('gb2312')
    headera = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Host': '210.37.0.22',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',

        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://210.37.0.22/',
    }
    url = 'http://210.37.0.22/default2.aspx'
    xx = requests.post(url, headers=headera, data=dat, cookies=ss)
    return s, user


def re(ss):
    u = 'http://210.37.0.22/xscj_gc.aspx?xh={}&xm=%D1%CF%B7%C7%B7%B2&gnmkdm=N121617'
    url = u.format(ss[1])
    header = {
        'Host': '210.37.0.22',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Length': '87041',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
    }
    heade = {
        'Host': '210.37.0.22',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://210.37.0.22/default2.aspx',
        'Connection': 'keep-alive',

    }
    oo = requests.get(url, headers=heade, cookies=ss[0].cookies)
    print(oo.text)
    sou = BeautifulSoup(oo.text, 'html.parser')
    view = sou.select('input[name="__VIEWSTATE"]')[0]['value']
    print(view)
    dat = {
        '__VIEWSTATEGENERATOR': '	DB0F94E3',
        '__VIEWSTATE': view,
        'Button1': ' % B0 % B4 % D1 % A7 % C6 % DA % B2 % E9 % D1 % AF'
    }
    res = requests.post(url, headers=header, data=dat, cookies=ss[0].cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def dw(soup):
    i = 0
    tit = []
    while True:
        link = soup.select('table#Datagrid1>tr')
        result = {}
        result['datatime'] = link[i].select('td')[0].contents[0]
        result['class'] = link[i].select('td')[3].contents[0]
        result['xscore'] = link[i].select('td')[6].contents[0]
        result['score'] = link[i].select('td')[8].contents[0]
        tit.append(result)
        i = i + 1
        if i == len(link):
            break
    return tit


def aa(tit):
    df = pandas.DataFrame(tit)
    df.to_excel('qqqqq.xls')


if __name__ == '__main__':
    pp = ff()
    xx = re(pp)
    mm = dw(xx)
    aa(mm)









