# scrapy 会自动的去重

import scrapy
from qq_news.items import DoubanBookItem

class BookSpider(scrapy.Spider):
  name = 'douban_book'
  # 主域名
  allowed_domain = ['douban.com']
  # 要爬取的起始url
  start_urls = ['https://book.douban.com/top250']
  
  # 解析函数 -> 通用模板
  def parse(self, response):
    # 取链接
    # 当前页 
    yield scrapy.Reaquest(response.url, callback = self.parse_page)

    for page in response.xpath('//div[@class="paginator"]/a'):
      link = page.xpath('@href').extract()[0]
      # 继续下一页
      yield scrapy.Request(link, callback = parse_page)

  # 解析页面函数 
  def parse_page(self, response):
    for item in response.xpath('//tr[@class="item"]'):
      # 初始化一本书
      book = DoubanBookItem()
      book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
      book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
      # 书籍信息
      book_info = item.xpath('td[2]/p[@class="pl"]/text()').extract()[0]
      book_info_contents = book_info.strip().split(' / ')
      book['author'] = book_info_contents[0]
      book['publisher'] = book_info_contents[1]
      book['edition_year'] = book_info_contents[2]
      book['price'] = book_info_contents[3]
      yield book                   
