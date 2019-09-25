# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class BilibiliPipeline(object):
    def open_spider(self,spider):
    #定义在爬虫开始时连接数据库的方法
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
    #定义item的处理方法
        sql = 'insert into bilibili(danmu) values("{}")'.format(item['danmu'])
        # 定义sql语句来插入数据弹幕的信息
        try:
            if self.cursor.execute(sql):
            #执行sql语句
                print("Successful")
                self.db.commit()
        except:
            print("Failed........")
            self.db.rollback()
        return item
    def spider_close(self,spider):
    #定义在爬虫结束时关闭数据库
        self.db.close()