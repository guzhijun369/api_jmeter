# coding=utf-8
import pymysql
from config.basic_config import ConfigInit
from loguru import logger

class HandleMySql:
    """数据库处理类"""
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=ConfigInit.mysql_host, port=ConfigInit.mysql_port, user=ConfigInit.mysql_user,
                                        password=ConfigInit.mysql_pw, db=ConfigInit.mysql_db, charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            logger.error('mysql连接失败，错误信息%s' %e)
        logger.info('连接mysql数据库{}:{}/{}'.format(ConfigInit.mysql_host,ConfigInit.mysql_port,ConfigInit.mysql_db))
        self.cursor = self.conn.cursor()

    def get_value(self, sql, args=None, is_more=False):
        """
        获取数据库的值
        :param sql: sql语句
        :param args: 其他参数
        :param is_more: 是否显示全部，默认显示一条数据
        :return: 字典为item的列表数据
        """
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        """关闭"""
        self.cursor.close()
        self.conn.close()
        logger.info('关闭数据库连接')

handle_sql = HandleMySql()
# if __name__ == '__main__':
#     handle_sql = HandleMySql()
#     sql = "select * from member where MobilePhone = %s;"
#     single_data = handle_sql.get_value(sql, "15828641020")
#     print(single_data)

