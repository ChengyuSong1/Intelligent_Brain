"""
192.168.3.158   boraydata2021
cd /data/rpdsql-ops
./rapids -P15333
"""
from utils.database_utils import MysqlDB
from sqlapi.settings import RPDSQL
import os
import json
import datetime


def getdate(num):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-num)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


if __name__ == "__main__":
    print(getdate(6*30))
    pass
    # with MysqlDB(database=RPDSQL) as cursor:
    #     sql = "select * from test_qiye;"
    #     cursor.execute(sql)
    #     rows = cursor.fetchall()
    #     print(rows)
    #     for row in rows:
    #         print(row)
    # print(os.path.exists("c:"))

    # p = os.path.join("c:/Users/wu/Desktop/1.朝阳区重点企业信息", "[静态].json")
    # data = json.loads(open(p, "r").read())
    # print(data)

    # 111.198.24.131:8888
