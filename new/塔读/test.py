import pandas as pd

data = pd.read_excel('tadu.xls', sheetname=u'CMS 书籍查询1')[u'书籍ID']
# 去重
_data = set(data)
for item in _data:
  print(item)
