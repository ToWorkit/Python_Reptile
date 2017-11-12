import asyncio

# 操作
@asyncio.coroutine
def wget(host):
  connect = asyncio.open_connection(host, 80)
  # 完成后返回
  # 走一次执行一次
  reader, writer = yield from connect 
  header = 'GET / HTTP/1.0\r\nHost: %s\r\n' % host
  # 写入header
  writer.write(header.encode('utf-8'))
  yield from writer.drain()
  while True:
    line = yield from reader.readline()
    if line == b'\r\n':
      break
    print('%s header --> %s' % (host, line.decode('utf-8').rstrip()))
  writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
 
