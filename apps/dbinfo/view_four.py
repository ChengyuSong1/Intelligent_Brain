import re
import os
import time
import json
import math
import random
import decimal
import datetime

from apps.baseview import BaseView
# from apps.dbinfo.models import DbInfos
from utils import idutils
from sqlapi.settings import RPDSQL, JSONDATA_PATH
from utils.database_utils import MysqlDB
from apps.dbinfo.utils import get_dict_key, get_color, get_five_year, get_random_bool, get_one_num, \
    get_random_num, get_ryb, get_random_color, getdate


# 4.1
class InputOutputStaticView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)
        last_year = year-1

        all_data = dict()
        data_dict = dict()
        data_dict1 = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  screen4 WHERE enterprise_name='{}' and year < 3000 order by year desc;".format(name)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                data_dict = rows[0]
            for one in rows:
                all_data[one["year"]] = one

            sql1 = "SELECT * FROM  screen4 WHERE enterprise_name='{}' and year=9999 order by year desc;".format(name)
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            if len(rows1) > 0:
                data_dict1 = rows1[0]

        five_years = get_five_year()

        sr_num1 = [get_dict_key(thedict=all_data.get(i, {}), key="district_tax_income", units=10000) for i in [i for i in range(last_year-4, last_year+1)]]
        zc_num1 = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund") for i in [i for i in range(last_year-4, last_year+1)]]

        sr_num2 = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund") for i in [i for i in range(last_year-4, last_year+1)]]
        zc_num2 = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund_rank") for i in [i for i in range(last_year-4, last_year+1)]]

        sr_num3 = [get_dict_key(thedict=all_data.get(i, {}), key="talent_service") for i in [i for i in range(last_year-4, last_year+1)]]
        zc_num3 = [get_dict_key(thedict=all_data.get(i, {}), key="talent_service_rank") for i in [i for i in range(last_year-4, last_year+1)]]

        sr_num4 = [get_dict_key(thedict=all_data.get(i, {}), key="housing_support") for i in [i for i in range(last_year-4, last_year+1)]]
        zc_num4 = [get_dict_key(thedict=all_data.get(i, {}), key="housing_support_rank") for i in [i for i in range(last_year-4, last_year+1)]]

        static = {
          # 企业名称
          "name": name,
          # 企业税收及服务排名分析
          "enterprise_tax_and_service_ranking": {
              # 企业服务管家负责领导及部门信息
              # "housekeeping_department": get_dict_key(thedict=data_dict, key="housekeeper"),
              # "department_leaders": get_dict_key(thedict=data_dict, key="district_governor"),
              # 六类指标排名蛛网图
              "six_kinds_ranking": {
                  "number":[
                   get_dict_key(thedict=data_dict, key="housing_support_rank"),    # 住房支持
                   get_dict_key(thedict=data_dict, key="talent_service_rank"),    # 人才服务
                   get_dict_key(thedict=data_dict, key="local_tax_income_rank"),  # 地方收入
                   get_dict_key(thedict=data_dict, key="tax_income_rank"),    # 税收排名
                   get_dict_key(thedict=data_dict, key="district_tax_income_rank"),    # 区级收入
                   get_dict_key(thedict=data_dict, key="support_fund_rank"),    # 资金支持
                    ],
                  "name": [
                      "住房支持排名",
                      "人才服务排名",
                      "地方级收入排名",
                      "税收排名",
                      "区级收入排名",
                      "资金支持排名",
                  ],

              },
              # 区级收入、资金支持趋势图
              "income_and_support": {
                        "year": [i for i in range(last_year-4, last_year+1)],
                        # 区级收入
                        "sr_num": sr_num1,
                        # 区级支持
                        "zc_num": zc_num1,
                        "sr_unit": "万元",
                        "zc_unit": "万元"
                    }
          },
          # 企业服务支持总体
          "es_support": {

            "support": {
                "number": [
                    get_dict_key(thedict=data_dict1, key="support_fund", num=0),                   # 引导资金支持
                    get_dict_key(thedict=data_dict1, key="overseas_talent_service_intro", num=0),  # 留学人才引进人数
                    get_dict_key(thedict=data_dict1, key="graduates_settlement", num=0),           # 应届生落户
                    get_dict_key(thedict=data_dict1, key="housing_support", num=0),                # 共有产权房优先人数
                    get_dict_key(thedict=data_dict1, key="work_and_residence_permit", num=0),      # 工作居住证办理量
                    get_dict_key(thedict=data_dict1, key="executive_talent_intro", num=0),         # 高管人才引进人数
                ],
                "title": [
                    "引导资金支持",
                    "留学人才引进人数",
                    "应届生落户数",
                    "共有产权房优先人数",
                    "工作居住证办理量",
                    "高管人才引进人数",
                ],
                "unit": [
                    "万",
                    "人",
                    "人",
                    "人",
                    "人",
                    "人",
                ],
            },
            # 服务包企业对比
            "contrast_support": {
                "our_company": get_dict_key(thedict=data_dict1, key="support_fund"),
                "service_package": get_dict_key(thedict=data_dict1, key="support_fund_ave"),
                "unit": "万元"
            },

            # 住房服务次数对比
            "house_support": {
              "our_company": get_dict_key(thedict=data_dict1, key="talent_service"),
              "service_package": get_dict_key(thedict=data_dict1, key="talent_service_ave"),
              "unit": "次"
            },
            # 人才服务次数对比
            "p_support": {
              "our_company": get_dict_key(thedict=data_dict1, key="housing_support"),
              "service_package": get_dict_key(thedict=data_dict1, key="housing_support_ave"),
              "unit": "次"
            },
          },
          # 企业服务支持变化
          "change_of_enterprise_service_support": {
              # 过去5年企业资金支持变化和排名变化
                 "m_support": {
                            "year": [i for i in range(last_year-4, last_year+1)],
                            # 政府资金支持额度
                            "sr_num": sr_num2,
                            # 获得政府资金支持额度的排名
                            "zc_num": zc_num2,
                            "unit": "万元"
                        },
              # 过去5年企业人才服务次数变化和排名变化
              "p_support": {
                  "year": [i for i in range(last_year-4, last_year+1)],
                  # 每年获得的人才服务次数
                  "sr_num": sr_num3,
                  # 人才服务次数的排名
                  "zc_num": zc_num3,
                  "unit": "次"
              },

              # 过去5年企业住房支持次数变化和排名变化
              "h_support": {
                  "year": [i for i in range(last_year-4, last_year+1)],
                  # 住房支持次数
                  "sr_num": sr_num4,
                  # 住房支持次数的排名
                  "zc_num": zc_num4,
                  "unit": "次"
              }

            }

        }

        return static


# 4.2
class VisitInfoView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        name = data.get("name", "")
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 6))

        static = {
          # 企业名称
          "name": name,
          "visit_information": [

          ]
        }

        tb = "screen4_ent_visit_info_list"

        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  {} WHERE enterprise_name='{}' order by visiting_time desc LIMIT {} OFFSET {};".format(tb, name,
                                                                                                      page_len, (
                                                                                                                  page - 1) * page_len)
            # print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()

            sql3 = "SELECT count(*) FROM  {} WHERE enterprise_name='{}'  order by visiting_time desc;".format(tb, name)

            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            total_num = rows3[0].get("count(*)")
            total_page = int(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

            satrt = 1 + page_len * (page - 1)
            for row in rows:
                static["visit_information"].append(
                    {
                        "code": satrt,
                        "qt_ld": get_dict_key(thedict=row, key="leading_leadership"),
                        # "gz_bm": get_dict_key(thedict=row, key="housekeeper"),
                        "gz_bm": get_dict_key(thedict=row, key="leading_department"),
                        "shi_you": get_dict_key(thedict=row, key="visiting_reason"),
                        "zf_time": get_dict_key(thedict=row, key="visiting_time"),
                        # "leading_leadership": get_dict_key(thedict=row, key="leading_leadership"),

                    }
                )
                satrt += 1
        # satrt = 1 + page_len * (page - 1)
        # nlist = ["张龙", "赵雷", "孙磊"]
        # for i in range(page_len):
        #     static["visit_information"].append(
        #         {
        #             "code": satrt,
        #             "gz_bm": "区发改委",
        #             "qt_ld": random.choice(nlist),
        #             "shi_you": "走访",
        #             "zf_time": "2020.06.01"
        #         }
        #     )
        #     satrt += 1

        # static["enterpriseLabel"] = list(static["enterpriseLabel"].values())
        result = {"page": page, "page_len": page_len, "total_num": 0, "total_page": 1, "data": static}
        return result