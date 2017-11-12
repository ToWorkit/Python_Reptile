import os
print('Process (%s) start' % os.getpid())
pid = os.fork()
# 子进程
if pid == 0: 
  print('子进程%s, 父进程id is %s' % (os.getpid(), os.getppid()) )
else:
  # 父进程
  print('父进程')
