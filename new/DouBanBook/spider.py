import urllib.request
from urllib import request
import re, xlwt, time

# 代理ip
proxy = '123.116.129.176'

# 伪装浏览器固定写法
req=urllib.request.Request("https://read.douban.com/provider/all")
# 请求头, 模仿浏览器
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
# 代理
proxy= urllib.request.ProxyHandler({'http':proxy})  
# 使用代理打开
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)  
urllib.request.install_opener(opener)
# 页面源码信息
html = urllib.request.urlopen(req).read()

# 正则对象
pattern = re.compile('<a href="(.*?)".*?provider-item">.*?avatar.*?src="(.*?)".*?name">(.*?)</div>.*?works-num">(.*?)部作品在售</div>.*?</a>', re.S)
# 获取内容
# 转为utf-8
content = re.findall(pattern, str(html, 'utf-8'))
# print(content)

'''写入excel操作'''
# 创建workbook和sheet对象
workbook = xlwt.Workbook()
# excel 底部 sheet1
# 覆盖单元格
sheet1 = workbook.add_sheet('统计', cell_overwrite_ok=True)
# 初始化excel样式
style = xlwt.XFStyle()
# 给样式创建字体
font = xlwt.Font()
font.name = 'Times New Roman'
font.bold = True

# 设置样式的字体
style.font = font
# 设置列宽
one_col = sheet1.col(1)
two_col = sheet1.col(2)
three_col = sheet1.col(3)
one_col.width = 500 * 20
two_col.width = 900 * 20
three_col.width = 400 * 20

# 在统计表中的第一行设置字段名称并写入数据
sheet1.write(0, 0, '序号', style)
sheet1.write(0, 1, '出版社_url', style)
sheet1.write(0, 2, 'LOGO_url', style)
sheet1.write(0, 3, '出版社名称', style)
sheet1.write(0, 4, '在售作品', style)

# 行号初始值
row = 0
# 在售数量初始值
sum = 0

for i in content:
  # 在第 row + 1 行第 1 列写入序号
  sheet1.write(row + 1, 0, row + 1, style)
  # 在第 row + 1 行第 2 列写入出版社_url
  sheet1.write(row + 1, 1, "https://read.douban.com{}".format(str(i[0])), style)
  # 在第 row + 1 行第 3 列写入LOGO_url
  sheet1.write(row + 1, 2, i[1], style)
  # 在第 row + 1 行第 4 列写入出版社名称
  sheet1.write(row + 1, 3, i[2], style)
  # 在第 row + 1 行第 5 列写入在售数量
  sheet1.write(row + 1, 4, int(i[3]), style)
  # 对在售数量求和
  sum += int(i[3])
  row += 1

  # 判断content列表是否遍历结束，并在sheet1表尾行写入在售数量求和的值
  if row == len(content):
    # 采集时间
    _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 生成excel命名的时间
    name_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 在表尾写入"合计"
    sheet1.write(row + 1, 3, '合计', style)
    # 在售数量累计值
    sheet1.write(row + 1, 4, sum, style)
    # 采集时间
    sheet1.write(row + 2, 3, '采集时间', style)
    # 时间
    sheet1.write(row + 2, 4, _time, style)

# 保存文件
workbook.save('./豆瓣阅读{}.xls'.format(str(name_time)))

print('写入完毕')
print('数据统计：{}'.format(str(sum)))
