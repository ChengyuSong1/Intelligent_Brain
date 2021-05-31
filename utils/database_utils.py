import sys
sys.path.append(".")
sys.path.append("..")

import pymysql


class MysqlDB(object):

    def __init__(self, database):
        """
        # __enter__() 和 __exit__() 是with关键字调用的必须方法
        :param database:
        """
        # 创建数据库连接
        self.dbconn = pymysql.connect(**database, charset='utf8')

        # 创建字典型游标(返回的数据是字典类型)
        self.dbcur = self.dbconn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        """
        # with本质上就是调用对象的enter和exit方法
        :return:
        """
        # 返回游标
        return self.dbcur

    def __exit__(self, exc_type, exc_value, exc_trace):
        # 提交事务
        self.dbconn.commit()
        # 关闭游标
        self.dbcur.close()
        # 关闭数据库连接
        self.dbconn.close()


if __name__ == "__main__":
    from sqlapi.settings import REDIS_CONFIG
