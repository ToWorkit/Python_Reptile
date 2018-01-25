import scrapy

# 定义类，需继承自scrapy.Spider
class StackOverFlowSpider(scrapy.Spider):
  # 命名，工程中必须唯一
  name = "stackoverflow"
  # 起始页
  start_urls = ['http://stackoverflow.com/questions?sort=votes']

  def __init__(self):
    pass

  # 解析页面
  def parse(self, response):
    # 通过css选择器获取到问题首页的所有文章的链接地址
    # a::attr(href) -> 属性值
    for href in response.css('.question-summary .summary h3 a::attr(href)'):
      # 链接是这样的(相对的)
      # /questions/11227809/why
      # 需要转为绝对的
      # https://stackoverflow.com/questions/11227809/why
      full_url = response.urljoin(href.extract())
      # print(href.extract(), full_url, '----------')
      # 生成器
      # 调用时给值
      # 将数据获取方法作为回调传入
      yield scrapy.Request(full_url, callback=self.parse_question)

  # 数据获取方法
  def parse_question(self, response):
    # ::text -> 获取文本
    # extract() -> list
    # print(response.css('.question .vote-count-post::text').extract(), '<<<<<<')
    yield {
      'title': response.css('#question-header > h1 > a::text').extract()[0],
      'votes': response.css('.question .vote-count-post::text').extract()[0],
      'body': response.css('.questions .post-text').extract()[0],
      'tags': response.css('.questions .post-tag::text').extract(),
      'link': response.url,  
    }
obj = StackOverFlowSpider()
