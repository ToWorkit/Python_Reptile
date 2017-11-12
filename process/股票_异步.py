import aiohttp
import asyncio

def get_stock(code):
  url = 'http://hq.sinajs.cn/list=' + code
  resp = yield from aiohttp.request('GET', url)

# 股票信息
codes = ['sz000878', 'sh600993', 'sz000002', 'sh600153', 'sz002230', 'sh600658']
# 创建线程
threads = [threading.Thread(target = get_stock, args = (code, )) for code in codes]
for t in threads:
  t.start()
# 等待每个线程的结束
for t in threads:
  t.join()
