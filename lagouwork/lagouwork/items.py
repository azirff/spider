# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouworkItem(scrapy.Item):
    industry = scrapy.Field()
    company = scrapy.Field()
    size = scrapy.Field()
    financing = scrapy.Field()
    city = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    work = scrapy.Field()
    wages = scrapy.Field()
    url = scrapy.Field()
    welfare = scrapy.Field()
    conditions = scrapy.Field()
