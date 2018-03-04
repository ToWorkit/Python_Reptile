import time
from multiprocessing import Process
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError
from proxypool.getter import FreeProxyGetter
from proxypool.setting import *
from asyncio import TimeoutError

# 检测代理是否可用
class ValidityTester(object):
    # 全局变量，使用百度做代理测试判断代理是否可用 -> setting.py
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        # 待检测的代理 list
        self._raw_proxies = proxies
        # 操作redis
        self._conn = RedisClient()

    # 异步检测
    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
            # 异步请求库 aiohttp
            async with aiohttp.ClientSession() as session:
                try:
                    # 判断proxy的类型
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    # 测试
                    # 测试地址，设置代理，设置超时
                    async with session.get(self.test_api, proxy=real_proxy, timeout=get_proxy_timeout) as response:
                        # 如果可用就加入到readis中(队列的右侧，方法在db.py中)
                        if response.status == 200:
                            self._conn.put(proxy)
                            print('Valid proxy', proxy)
                # 无效代理
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print(s)
            pass

    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            # 调用异步检测
            loop = asyncio.get_event_loop()
            # 检测每个代理
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            # 异步 wait 放入redis中
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Async Error')


class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        # 检测代理是否可用的类
        self._tester = ValidityTester()
        # 抓取代理的类 -> getter.py
        self._crawler = FreeProxyGetter()

    # 判断代理池有没有达到上界
    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    # 添加代理的操作
    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        # 判断代理池有没有达到上界
        while not self.is_over_threshold():
            # 获取代理抓取方法的数量进行遍历
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                # 依次取出获取代理方法的名称
                callback = self._crawler.__CrawlFunc__[callback_label]
                # 根据抓取代理的方法名执行方法获取代理
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                # 取出代理加入到右侧进行测试并更新
                self._tester.set_raw_proxies(raw_proxies)
                # 将测试通过的代理放入redis中
                self._tester.test()
                # 更新代理的数量
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    # 参数 -> 时间(定时检查)
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """
        Get half of proxies which in redis
        """
        # redis 连接对象 -> db.py 文件中
        conn = RedisClient()
        # 检测代理是否可用的类
        tester = ValidityTester()
        while True:
            print('Refreshing ip')
            # 取出redis队列中一半的代理(左侧)
            count = int(0.5 * conn.queue_len)
            # 队列数据为0时等待一会(抓取器会一直在抓取)
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            # 取出代理加入到右侧进行检测并更新
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    # 抓取代理
    # 代理池数量界限
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD, 
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   # 轮询的间隔时间
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            # 小于代理池下限就重新抓取
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        print('Ip processing running')
        # 两个进程
        # 定时从redis数据库中检测代理
        valid_process = Process(target=Schedule.valid_proxy)
        # 从网上获取代理并进行筛选后放入redis库中
        check_process = Process(target=Schedule.check_pool)
        # 开始进程
        valid_process.start()
        check_process.start()
