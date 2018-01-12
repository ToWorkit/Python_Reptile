import urllib.request
# 线程
import threading
import re
import urllib.error
# 模仿浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)

# 多线程开启后会并发执行(会出现两个线程交替执行的情况)

# 创建一个线程
# 需要继承自threading.Thread
class One(threading.Thread):
  def __init__(self):
    # 初始化线程
    threading.Thread.__init__(self)
  # 线程启动方法
  def run(self):
    # 一个线程爬取单数页
    for i in range(1, 36, 2):
      url="http://www.qiushibaike.com/8hr/page/"+str(i)
      # utf-8转码，忽略特殊编码
      pagedata=urllib.request.urlopen(url).read().decode("utf-8","ignore")
      pat='<div class="content">.*?<span>(.*?)</span>.*?</div>'
      # 正则查找
      datalist=re.compile(pat,re.S).findall(pagedata)
      # 提取内容
      for j in range(0, len(datalist)):
        print("第{}页，第{}个段子内容".format(str(i), str(j)))
        print(datalist[j])
# 创建第二个线程
class Two(threading.Thread):
  def __init__(self):
    # 初始化线程
    threading.Thread.__init__(self)
  # 线程启动方法
  def run(self):
    # 第二个线程爬取偶数页
    for i in range(0, 36, 2):
      url="http://www.qiushibaike.com/8hr/page/"+str(i)
      # utf-8转码，忽略特殊编码
      pagedata=urllib.request.urlopen(url).read().decode("utf-8","ignore")
      pat='<div class="content">.*?<span>(.*?)</span>.*?</div>'
      # 正则查找
      datalist=re.compile(pat,re.S).findall(pagedata)
      # 提取内容
      for j in range(0, len(datalist)):
        print("第{}页，第{}个段子内容".format(str(i), str(j)))
        print(datalist[j])

# 实例化
one = One()
two = Two()
# 开启线程
one.start()
two.start()
