import re
import requests
from bs4 import BeautifulSoup

'''
先爬取东方财富的股票代码，再根据股票代码爬取百度股市通的股票详情
'''
class Spider(object):
  def __init__(self):
    self.headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }

  # 页面爬取公共代码
  def getPage(self, url):
    try:
      r = requests.get(url=url, headers=self.headers)
      # 判读页面是否返回正确
      # HttpError -> https://www.jianshu.com/p/159bea26f7b5
      r.raise_for_status()
      # 使用源网站编码
      r.encoding = r.apparent_encoding
      # 返回BeautifulSoup对象
      return BeautifulSoup(r.text, 'html.parser')
    except:
      print('HTTPError 连接错误')
      return None
