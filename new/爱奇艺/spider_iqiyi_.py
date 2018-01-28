import requests
import re
from bs4 import BeautifulSoup as bs

class Main(object):
  def __init__(self, target):
    self._target_url = target
    self._head = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }
  def get_book_total_chapter(self):
    response = requests.get(url=self._target_url, headers=self._head)
    response.encoding = 'utf-8'
    # print(response.text)
    html_data = response.text
    # 构建BeautifulSoup对象
    chapter_obj = bs(html_data, 'html.parser')
    # 找到章节容器
    chapter_cont = chapter_obj.find_all('dl', class_="catalog-list")
    chapter = []
    # 找到所有的章节
    chapter_str = chapter_cont[0].find_all('dd', class_='clearfix')
    # print(chapter_cont)
    for item in chapter_str:
      chapter.append(item.a.string)
    print(chapter)

url = 'http://wenxue.iqiyi.com/book/catalog-18l2h0jzxl-1.html'
obj = Main(target = url)
obj.get_book_total_chapter()
