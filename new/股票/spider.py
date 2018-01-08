import re
import requests
import json
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

  # 东方财富股票代码号
  def eastMoney(self):
    url = 'http://quote.eastmoney.com/stocklist.html'
    html_data = self.getPage(url)
    # 股票代码容器
    quotesearch = html_data.find_all('div', id='quotesearch')
    # print(quotesearch)
    # 获取代码
    a_list = []
    a_item = map(lambda x: x.find_all('a'), quotesearch)
    for i in list(a_item)[0]:
      # print(i.attrs['href'])
      try:
        if i.attrs['href'] is not None:
          href = i.attrs['href']
          # print(href)
          a_list.append(re.findall(r'[s][hz]\d{6}', href)[0])
      except:
        # print('获取代码出错')
        # 跳过不符合的项
        continue
    return a_list
  # 根据获取的股票代码抓取百度股市通的股票详情
  def getStockDetails(self, stock_list):
  # def getStockDetails(self):
    '''url = 'https://gupiao.baidu.com/stock/sh000001.html'
    html_data = self.getPage(url)
    
    stock_bets = html_data.find('div', attrs={'class': 'stock-bets'})
    name = stock_bets.find('a', attrs={'class': 'bets-name'})
    stock_data = {}
    stock_data.update({'名称': name.text.strip()})
    stock_data['list'] = []
    # 参数项
    bets_content_col = stock_bets.find('div', attrs={'class': 'bets-col-9'})
    for i in bets_content_col.find_all('dl'):
      _list = {}
      _list['name'] = i.find('dt').text
      _list['value'] = i.find('dd').text
      stock_data['list'].append(_list)
    print(stock_data)'''

    
    url = 'https://gupiao.baidu.com/stock/{}.html'
    stock_data = {}
    stock_data['list'] = []
    for i in stock_list:
      html_data = self.getPage(url.format(i))
      # 容错处理
      try:
        if html_data == "":
          continue
        # find
        stock_bets = html_data.find('div', attrs={'class': 'stock-bets'})
        name = stock_bets.find('a', attrs={'class': 'bets-name'})
        # 添加
        stock_data.update({'名称': name.text.strip()})
        # 参数项
        bets_content_col = stock_bets.find('div', attrs={'class': 'bets-content'})
        for i in bets_content_col.find_all('dl'):
          _list = {}
          _list['name'] = i.find('dt').text
          _list['value'] = i.find('dd').text
          stock_data['list'].append(_list)
        with open('Stock.txt', 'a', encoding='utf-8') as f:
          # 不进行ascii转码(不设置中文会自动被转为ASCII码)
          f.write(json.dumps(stock_data, ensure_ascii=False) + '\n')
      except:
        print('有错误')
        continue
    # print(stock_data)

    
  # 主函数
  def main(self):
    # self.eastMoney()
    self.getStockDetails(self.eastMoney()[100: 102])
    # self.getStockDetails()

if __name__ == '__main__':
  main = Spider().main()
