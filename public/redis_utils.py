# coding=utf-8
import redis
from config.basic_config import ConfigInit
from loguru import logger

class MyRedis:

    def __init__(self):
        try:
            self.r = redis.StrictRedis(host=ConfigInit.redis_host, port=ConfigInit.redis_port,
                                    db=ConfigInit.redis_db, password=ConfigInit.redis_pw, decode_responses=True)
        except Exception as e:
            logger.error('redis连接失败，错误信息%s' %e)

    def str_get(self, k):
        res = self.r.get(k)
        if res:
            return res

    def str_set(self, k ,v, time=None):
        self.r.set(k, v, time)

    def delete(self, k):
        tag = self.r.exists(k) #判断这个Key是否存在
        if tag:
            self.r.delete(k)
            logger.debug('删除成功')
        else:
            logger.debug('这个key不存在')
    def hash_hget(self, name, key):
        res = self.r.hget(name, key)
        if res:
            return res

    def hash_hset(self,name, k, v):
        self.r.hset(name, k, v)

    def hash_del(self, name,k):
        res = self.r.hdel(name, k)
        if res:
            logger.debug('删除成功')
            return True
        else:
            logger.debug('删除失败.该key不存在')
            return False

    def key_expire(self, k ,t):
        self.r.expire(k, t)

if __name__ == '__main__':
    redis_con = MyRedis()
    # redis_con.str_set('Phone_code', '123456')
    r = redis_con.hash_hget('phone_code', '13028812388')
    # redis_con.hash_hset('phone_code', '13028812388', '123456')
    # redis_con.key_expire('phone_code', 60)
    print(r)