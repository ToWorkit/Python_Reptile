from proxypool.api import app
from proxypool.schedule import Schedule

def main():
    # 调度器
    s = Schedule()
    s.run()
    # api flask接口返回数据
    app.run()




if __name__ == '__main__':
    main()

