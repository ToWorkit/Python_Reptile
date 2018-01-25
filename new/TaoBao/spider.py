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
# 配置
from config import *
# mongo
import pymongo
chromeOptions = webdriver.ChromeOptions()
# 连接
client = pymongo.MongoClient(MONGO_URL)
# 获取游标
db = client[MONGO_DB]
# 设置代理
# chromeOptions.add_argument("--proxy-server=183.186.86.171:80")
# 启动
# browser = webdriver.Chrome(chrome_options = chromeOptions)
browser = webdriver.Chrome()
# 等待
wait = WebDriverWait(browser, 10)

# 查看本机ip，查看代理是否起作用
# browser.get("http://httpbin.org/ip")
# print(browser.page_source)


def search():
  try:
    # 打开淘宝
    # 天猫的下一页居然要登录，后期做(╯‵□′)╯︵┻━┻
    browser.get('https://www.taobao.com')
    # 等待页面渲染后获取到id值为 q 的元素
    input = wait.until(
      # css 选择器方式 
      # 等待页面渲染后
      EC.presence_of_element_located((By.CSS_SELECTOR, "#q",))
    )
    # 等待按钮为可点击状态
    submit = wait.until(
      # 等待按钮可点击
      # 参数为tuple元组
      EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button',))
    )
    # 要搜索值
    input.send_keys('迪奥')
    # 点击搜索按钮
    submit.click()
    # 等待页数加载完毕
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
    get_products()
    # print(total.text)
    return total.text
  except Exception:
    print('获取页数出错')
    return search()

# 翻页
def next_page(page_num):
  try:
    # 等待页面渲染
    input = wait.until(
      # css 选择器方式 
      # 翻页输入框
      EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input",))
    )
    # 等待按钮为可点击状态
    # 确定翻页按钮
    submit = wait.until(
      # 等待按钮可点击
      # 参数为tuple元组
      EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit',))
    )
    # 先清空再写
    input.clear()
    # 等待当前选中的页码 和 输入的页码 值一致时的页面加载时先给定 新值，再继续等待上一页的页码对应页面加载
    input.send_keys(page_num)
    time.sleep(2)
    submit.click()
    # 找到当前的页码元素
    # text_to_be_present_in_element
    # 等待当前选中的页码 和 输入的页码 值一致时的页面加载完毕
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num)))
    get_products()
  except Exception:
    print('翻页出错了')
    return next_page(page_num)

# 解析抽取数据
def get_products():
  # 找到内容标签
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
  # 获取页面内容
  html = browser.page_source
  # 构建PyQuery对象
  doc = pq(html)
  # 获取所有的
  items = doc('#mainsrp-itemlist .items .item').items()
  # print(items)
  for item in items:
    product = {
      # 获取属性值
      'image': item.find('.pic .img').attr('src'),
      # 获取内容
      'price': item.find('.price').text(),
      # 去掉后三个字
      'deal': item.find('.deal-cnt').text()[:-3],
      'title': item.find('.title').text(),
      'shop': item.find('.shop').text(),
      'location': item.find('.location').text()
    }
    save_to_mongo(product)

# 保存到数据库
def save_to_mongo(result):
  try:
    # 插入数据
    if db[MONGO_TABLE].insert(result):
      print("储存成功", result)
  except Exception:
    print('存储失败', result)

def main():
  search()

  # total = search()
  # 提取页数
  # total = int(re.compile('(\d+)').search(total).group(1))
  # 翻页
  # for i in range(2, total + 1):
  #   next_page(i)
  # 执行完毕后关闭浏览器
  # browser.close()

if __name__ == '__main__':
  main()
