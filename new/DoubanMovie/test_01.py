import requests
import re
from bs4 import BeautifulSoup as bs

headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

''' 获取电影信息 '''
def get_movie_details():
  url = 'https://movie.douban.com/cinema/nowplaying/beijing/'
  # 构建请求并接收响应
  response = requests.get(url=url, headers=headers)
  response.encoding = 'utf-8'
  # print(response.text)
  html_data = response.text
  # 构建BeautifulSoup对象
  soup_obj = bs(html_data, 'html.parser') 
  # 找到正在上映的电影信息标签 -> list格式
  nowplaying_movie = soup_obj.find_all('div', id='nowplaying')
  # print(nowplaying_movie)
  # 找到电影信息列表的li
  nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
  # 获取电影id，根据电影图片获取电影名称
  # print(nowplaying_movie_list)
  nowplaying_list = []
  for item in nowplaying_movie_list:
    # print(item['data-actors'])
    # print(item)
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
      nowplaying_dict['name'] = tag_img_item['alt']
      nowplaying_list.append(nowplaying_dict)
  return nowplaying_list

''' 获取电影评论信息 '''
def get_movie_comment():
  movie_id = get_movie_details()[0]['id']
  url = 'https://movie.douban.com/subject/' + movie_id + '/comments?start=0&limit=20'
  response = requests.get(url=url, headers=headers)
  response.encoding = 'utf-8'
  html_data = response.text
  # 构建BeautifulSoup对象
  soup_obj = bs(html_data, 'html.parser')
  # 找到评论标签
  comment_conent = soup_obj.find_all('div', class_='comment')
  # 获取到评论内容
  eachCommentList = []
  for item in comment_conent:
    # find_all -> list
    if item.find_all('p')[0].string is not None:
      eachCommentList.append(item.find_all('p')[0].string)
  return eachCommentList


''' 数据清洗 '''
def data_cleaning():
  comments = ''
  comment_data = get_movie_comment()
  for k in range(len(comment_data)):
    comments = comments + (str(comment_data[k])).strip()
  # 去掉标点符号
  pattern = re.compile(r'[\u4e00-\u9fa5]+')
  filter_data = re.findall(pattern, comments)
  # 清洗后的数据
  cleaned_comments = ''.join(filter_data)
  return cleaned_comments

# 结巴分词
import jieba
import pandas as pd

# 分割 -> 直接返回 list
segment = jieba.lcut(data_cleaning())
# 生成表格
words_df = pd.DataFrame({'segment': segment})
# 去除停用词(高频出现的词)
# https://www.cnblogs.com/datablog/p/6127000.html -> 参数说明
stopwords = pd.read_csv('StopWords.txt', index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

# 词频统计
import numpy
words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数': numpy.size})
words_stat = words_stat.reset_index().sort_values(by=['计数'], ascending=False)
