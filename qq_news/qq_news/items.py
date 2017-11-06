# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义需要的item -> 处理在pipelines中
class QqNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #  标题
    title = scrapy.Field()
    # 内容
    text = scrapy.Field()
    # 来源
    source = scrapy.Field()
