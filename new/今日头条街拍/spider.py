import json
import os
import re
# 将对象参数准换为请求参数 => {'name': 1, 'age: 2'} -> name=1&age=2
from urllib.parse import urlencode
# mongo 连接
import pymongo
import requests
from bs4 import BeautifulSoup
# 处理连接错误
from requests.exceptions import ConnectionError
# 进程池
from multiprocessing import Pool
# md5 防重复
from hashlib import md5
# json 解码错误
from json.decoder import JSONDecodeError
# 配置文件
from config import *

# 建立mongo连接，忽略重复连接警告
client = pymongo.MongoClient(MONGO_URL, connect=False)
# 连接数据库并获取到游标
db = client[MONGO_DB]


'''
请求接口获取数据
'''
def get_page_index(offset, keyword):
  data = {
    'autoload': 'true',
    'count': 20,
    'cur_tab': 3,
    'format': 'json',
    'keyword': keyword,
    'offset': offset, # 下拉获取所需参数
  }
  # 处理参数
  params = urlencode(data)
  base = 'http://www.toutiao.com/search_content/'
  url = base + '?' + params
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.text
    return None
  except ConnectionError:
    print('连接错误')
    return None
'''
解析数据获取图片文章页面的url
'''
def parse_page_index(text):
  try:
    # 转为python对象
    data = json.loads(text)
    if data and 'data' in data.keys():
      for item in data.get('data'):
        # 生成器方式，调用才会给值
        # 获取图片文章页面的url
        yield item.get('article_url')
  except:
    print('json.loads()解析错误')
    return None


'''
请求图片文章页面地址
'''
def get_page_detail(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.text
    return None
  except ConnectionError:
    print('连接错误')
    return None
'''
解析文章页面获取图片信息
'''
def parse_get_detail(html):
  # 图片数据正则对象
  img_pattern = re.compile('BASE_DATA.galleryInfo = (.*?)</script>', re.S)
  result = re.search(img_pattern, html) 
  if result:
    # data_js = json.dumps()
    data = json.dumps(result.group(1))
    print(json.loads(data.decode('utf-8').replace("'", "\"")))
    # if data and 'gallery' in data.keys():
    #   gallery = data.get('gallery')
    #   print(gallery)
      # images = [item.get('url') for item in sub_images]
for i in parse_page_index(get_page_index(3, '街拍')):
  parse_get_detail(get_page_detail(i))
  # print(get_page_detail(i))
  # print(get_page_detail(i))
