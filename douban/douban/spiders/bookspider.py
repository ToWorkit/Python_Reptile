# -*- coding:utf-8 -*-
'''by sudo rm -rf  http://imchenkun.com'''
import scrapy
from douban.items import DoubanBookItem
# scrapy 会自动的去重

class BookSpider(scrapy.Spider):
    name = 'douban-book'
    # 主域名
    allowed_domains = ['douban.com']
    # 要爬取的起始url
    start_urls = [
        'https://book.douban.com/top250'
    ]

    # 解析函数 -> 通用模板
    def parse(self, response):
        # 请求第一页
        # 取链接
        # 当前页 
        yield scrapy.Request(response.url, callback=self.parse_next)

        # 请求其它页
        for page in response.xpath('//div[@class="paginator"]/a'):
            link = page.xpath('@href').extract()[0]
            # 继续下一页
            yield scrapy.Request(link, callback=self.parse_next)
    # 解析页面函数 
    def parse_next(self, response):
        for item in response.xpath('//tr[@class="item"]'):
            # 初始化一本书
            book = DoubanBookItem()

            # 需要的信息
            book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
            book['content'] = item.xpath('td[2]/p/text()').extract()[0]
            book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
            yield book
