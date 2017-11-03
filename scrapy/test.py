# 命令行
# -o -> 保存至
# scrapy runspider test.py -o test.json
import scrapy
# 先定义一个蜘蛛的类
# 继承自 scrapy 的 Spider
class QuoteSpider(scrapy.Spider):
    name = 'quote'
    # 起始页 -> 可以是多个
    # 1 - 20 页
    start_urls = ['http://quotes.toscrape.com/tag/humor/']
    
    # 解析
    def parse(self, response):
        # 找到所有 div.class = course_info_box 的元素
        for quo in  response.xpath('//div[@class="quote"]'):
            # 推荐数
            print(quo.xpath('span[@class="text"]/text()').extract_first())
            print(quo.xpath('span/small[@class="author"]/text()').extract_first())
            yield {
                'title': quo.xpath('span[@class="text"]/text()').extract_first(),
                'author': quo.xpath('span/small[@class="author"]/text()').extract_first(),
            }
        # 下一页操作
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # 最后一页木有下一页
        if next_page is not None:
            # 不为空就加入到 爬取url队列 中
            next_page = response.urljoin(next_page)
            # 加入执行操作
            # 回调函数 -> 递归自己
            # 当前页继续使用parse函数解析
            yield scrapy.Request(next_page, callback = self.parse)
