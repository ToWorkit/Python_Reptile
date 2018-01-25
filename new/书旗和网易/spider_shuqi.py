import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 类似jQuery的解析器
from pyquery import PyQuery as pq
# mongo
import pymongo
# chromeOptions = webdriver.ChromeOptions()
# 连接
# client = pymongo.MongoClient(MONGO_URL)
# 获取游标
# db = client[MONGO_DB]
# 设置代理
# chromeOptions.add_argument("--proxy-server=183.186.86.171:80")
# 启动
# browser = webdriver.Chrome(chrome_options = chromeOptions)
# 等待
# wait = WebDriverWait(browser, 10)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 30)
# 章节列表
chapter_list = []

class Chapter():
  def __init__(self, target):
    # 获取页面内容
    # html = browser.page_source
    # # 构建PyQuery
    # doc = pq(html)
    # 打开页面等待加载
    browser.get(target)
    time.sleep(5)
    __html = browser.page_source
    self.doc = pq(__html)
  # 解析
  def parse(self):
    try:
      # 等待章节列表加载完成
      wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#page-chapter-list > div.chapter-list-content > div', ))
      )
      # 获取章节列表
      items = self.doc('.chapter-list-content .chapter-list .chapter-item').items()
      chapter_list_one = []
      # print(items, '---')
      for item in items:
        # print(item.children().eq(0).html(), '---')
        chapter_list_obj = {
          'name': item.children().eq(0).html(),
          'url': 'http://t.shuqi.com/route.php?pagename=' + item.attr('href')
        }
        chapter_list_one.append(chapter_list_obj)
      # print(chapter_list)
      # 执行完毕后关闭浏览器
      # browser.close()
      return chapter_list_one
    except Exception as e:
      print(e)

  def select(self):
      # 等待下拉按钮可点击
      select_ = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#page-chapter-list > div.chapter-list-content > div > div.chapter-range', ))
      )
      # 点击下拉
      select_.click()
      # 等待下拉后的选择框加载
      wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.bs-modal.modal-in > div.modal-content > div',))
      )
      time.sleep(2)
      # 获取页面内容
      html = browser.page_source
      check_doc = pq(html)
      items = check_doc('.bs-modal .modal-content .check-list').children()
      # 4
      count = len(items)
      return count
      # for item in items:
      #   print(item)
      # print(len(items), '---')
      # for i in range(1, count):
      #   items[i].click()
  # 选择章节段   
  def check_con(self):
    count = self.select()
    for i in range(2, count):
      check_item = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.bs-modal.modal-in > div.modal-content > div > div:nth-child({})'.format(i), ))
      )
      check_item.click()
      time.sleep(2)
      chapter_list_one_ = self.parse()
      chapter_list.append(chapter_list_one_)
      self.select()
    # 执行完毕后关闭浏览器
    browser.close()
if __name__ == '__main__':
  url = 'http://t.shuqi.com/route.php?pagename=#!/ct/chapterList/bid/7111581'
  chapter = Chapter(target=url)
  # chapter.parse()
  chapter.check_con()
  print(chapter_list)

  # 获取的章节还是有bug的，待处理
