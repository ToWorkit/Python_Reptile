import time
import threadpool

def long_op(n):
  print(n)
  # 延迟2秒
  time.sleep(2)

# 创建相应的线程池
# 4 -> 处理的个数
pool = threadpool.ThreadPool(3)
# 函数，任务
tasks = threadpool.makeRequests(long_op, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(len(tasks))
# 将任务放入线程池
[pool.putRequest(task) for task in tasks]
pool.wait() 
