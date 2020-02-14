# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LagouworkPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='xx', port=3306)
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        sql = 'insert into lagouwork(city,experience,education,wages,work,url,welfare,conditions,company,size,financing,industry) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            item['city'], item['experience'], item['education'], item['wages'], item['work'], item['url'], item['welfare'], item['conditions'], item['company'], item['size'], item['financing'],
            item['industry']);  # 插入数据库的SQL语句
        try:
            if self.cursor.execute(sql):
                print("Successful")
                self.db.commit()
        except:
            print("Failed........")
            self.db.rollback()
        return item
    def spider_close(self,spider):
        self.db.close()