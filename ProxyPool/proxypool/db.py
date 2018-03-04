import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD

# redis 操作
class RedisClient(object):
    # 连接
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    # 
    def get(self, count=1):
        """
        get proxies from redis
        """
        # redis 队列有左右之分
        # 从队列的左侧获取数据 => 目的，左侧获取并留存数据，右侧检测并储存左侧留存的数据，使得右侧数据始终新于左侧
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        # 检测成功将数据放到右侧
        self._db.rpush("proxies", proxy)

    def pop(self):
        """
        get proxy from right.
        """
        # 从右侧(最新的)拿出可用代理
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        # 获取队列的长度
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        # 刷新整个代理
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
