import urllib.request
from urllib import request
import re, xlwt, time

# 代理ip
proxy = '123.116.129.176'

# 伪装浏览器固定写法
req=urllib.request.Request("https://read.douban.com/provider/all")
# 请求头
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
# 代理
proxy= urllib.request.ProxyHandler({'http':proxy})  
# 使用代理打开
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
urllib.request.install_opener(opener)
# 页面源码信息
html = urllib.request.urlopen(req).read()

# 正则对象
pattern = re.compile('<li><a href="(.*?)".*?provider-item">.*?avatar.*?src="(.*?)".*?name">(.*?)</div>.*?works-num">(.*?)部作品在售</div>.*?</a></li>', re.S)
# 获取内容
# 转为utf-8
content = re.findall(pattern, str(html, 'utf-8'))
print(content)
