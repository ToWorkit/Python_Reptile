import requests
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
  eachCommentList
