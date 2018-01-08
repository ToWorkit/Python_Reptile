import json
_list = [1, 2, 3, 4]
item = map(lambda x : x, _list)
a = list(item)
print(a)

url = 'https://gupiao.baidu.com/stock/{}.html'
print(url.format(12))

data = {'名称': '上证指数 (000001)', 'list': [{'name': '最高', 'value': '3412.73'}, {'name': '最低', 'value': '3384.56'}, {'name': '今开', 'value': '3391.55'}, {'name': '昨收', 'value': '3391.75'}, {'name': '成交额', 'value': '2639.13亿'}, {'name': '成交量', 'value': '2.18亿手'}, {'name': '涨家数', 'value': '589'}, {'name': '跌家数', 'value': '693'}, {'name': '平家数', 'value': '107'}]}

print(json.dumps(data, ensure_ascii=False))


_list = [1, 2, 3, 4, 5]
print(_list[2:3])
