from multiprocessing import Process
import os
def run_proc(name):
  # 子进程号
  print('Run child process %s (%s)' % (name, os.getpid()))
if __name__ == '__main__':
  # 父进程号
  print('Parent process %s' % os.getpid())
  # 创建进程
  p = Process(target = run_proc, args = ('test', ))
  # 开始
  p.start()
  # 等待结束
  p.join()
  print('end')
