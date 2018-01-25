import re
import time
# https://seleniumhq.github.io/selenium/docs/api/py/api.html
# http://www.cnblogs.com/mengyu/category/950040.html
# http://selenium-python.readthedocs.io/api.html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 类似jQuery的解析器
from pyquery import PyQuery as pq
import pandas as pd
import pymongo
from config import *
# 连接mongo
client = pymongo.MongoClient(MONGO_URL)
# 获取数据库游标
db = client[MONGO_DB]

class Spider():
  def __init__(self):
    # 书籍信息
    self.bookMessage = {}
    # 章节列表
    self.chapter = []
    # 浏览器
    self.browser = None
    # 等待操作
    self.wait = None
  def excelBookId(self):
    # 读取excel文件sheet名为CMS..的书籍ID栏
    data = pd.read_excel('tadu.xls', sheetname=u'CMS 书籍查询1')[u'书籍ID']
    # 去重
    _data = set(data)
    for item in _data:
      # 睡2秒
      time.sleep(2)
      self.book(item)
      # 全部获取到再存储到mongo
      self.saveToMongo(self.bookMessage)
  # 获取书籍信息
  def book(self, book_id):
    try:
      # print(book_id)
      # 启动
      self.browser = webdriver.Chrome()
      # 等待
      self.wait = WebDriverWait(self.browser, 10)
      # 打开页面
      self.browser.get('http://m.tadu.com/book/%s' % book_id)
      # 等待元素加载
      section = self.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#content > section.book-intro', ))
      )
      # css选择器
      # _id -> 解决mongo的id重复报错问题
      self.bookMessage['_id'] = str(book_id)
      self.bookMessage['book_name'] = section.find_element_by_css_selector('#content > section.book-intro > a.book-name').text
      self.bookMessage['book_summary'] = section.find_element_by_css_selector('#content > section.book-intro > div.intro > p').text
      self.bookMessage['book_keywords'] = section.find_element_by_css_selector('#content > section.book-intro > div.book-type > ul > li').text
      # 等待更多章节加载
      more = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > section.book-catalog > a.more-chapter',))
      )
      # 点击操作
      more.click()
      time.sleep(2)
      self.parse()
      time.sleep(2)
      self.nextPage()
    except Exception as err:
      print(err, '--------')
  # 翻页
  def nextPage(self):
    try:
      # 等待下一页按钮为可点击状态
      input = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#container > div.setHeight > section > div.chapter_b > input.next',))
      )
      input.click()
      time.sleep(1)
      # 解析当前页面内容
      self.parse()
    except Exception as err:
      print(err, '----')
  # 解析函数
  def parse(self):
    # 等待章节内容标签加载
    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container > div.setHeight > section > ul', )))
    # 获取页面内容
    html = self.browser.page_source
    # 构建PyQuery对象
    doc = pq(html)
    # css选择器获取章节容器
    items = doc('.chapter_ul').items()
    # 需要迭代获取数据
    for item in items:
      time.sleep(1)
      # 添加至章节列表
      self.chapter.append(item.text())
    # 完成后将章节放入书籍信息中
    # self.bookMessage['chapter_content'] = self.chapter
    time.sleep(2)
    self.nextPage()
  # 保存到数据库
  def saveToMongo(self, result):
    # 完成后将章节放入书籍信息中
    self.bookMessage['chapter_content'] = self.chapter
    print(result['book_name'])
    try:
      if db[MONGO_TABLE].insert(result):
        print('存储成功')
        # 执行完毕后关闭浏览器
        self.browser.close()
    except Exception as err:
      print('储存失败', err)

    
if __name__ == '__main__':
  spider = Spider()
  spider.excelBookId()
