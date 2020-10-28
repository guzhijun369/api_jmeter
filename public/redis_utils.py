# coding=utf-8
import redis
from config.basic_config import ConfigInit

redis_store = None


def con_redis():  # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=ConfigInit.redis_host, port=ConfigInit.redis_port,
                                    db=ConfigInit.redis_db, decode_responses=True)


def get_redis():  # 输出连接池
    con_redis()
    return redis_store


# if __name__ == '__main__':
#     con_redis()
#     print(get_redis())