# coding=utf-8

import pymysql

from config.basic_config import ConfigInit


def connect_sql():
    con = pymysql.connect(host=ConfigInit.mysql_host, port=ConfigInit.mysql_port, user=ConfigInit.mysql_user,
                          password=ConfigInit.mysql_pw, db=ConfigInit.mysql_db, charset='utf8mb4')
    # con.autocommit(False)
    print('连接数据库成功')
    return con


# if __name__ == '__main__':
#     print(connect_sql())
