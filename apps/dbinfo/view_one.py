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


# 1.1
class InfoStaticView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))

        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        five_years = [i for i in range(year-5, year)]
        all_data = dict()
        data_dict = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "select * from screen1 where YEAR IN ({}) order by year desc;".format(",".join([str(i) for i in five_years]))
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                data_dict = rows[0]
            for one in rows:
                all_data[one["year"]] = one

        q_num = [get_dict_key(thedict=all_data.get(i, {}), key="district_tax_income", units=10000*10000) for i in five_years]
        z_num = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund") for i in five_years]

        static = {
          # 模块1， 朝阳区服务包企业基本信息
          "EnterpriseInfo": {
            "number": [
              get_dict_key(thedict=data_dict, key="enterprise_number"),  # 企业数量
              get_dict_key(thedict=data_dict, key="local_tax_income", units=10000*10000),  # 地方级收入总量
              get_dict_key(thedict=data_dict, key="local_tax_income_by_district_rate"),  # 地方级收入占全区地方级收入比
              get_dict_key(thedict=data_dict, key="district_tax_income", units=10000*10000),  # 企业区级收入总量
              get_dict_key(thedict=data_dict, key="district_tax_income_by_district_rate"),  # 区级收入占全区区级收入比
              get_dict_key(thedict=data_dict, key="support_fund"),                          # 企业资金支持金额总量
              get_dict_key(thedict=data_dict, key="support_fund_by_district_rate", units=0.01),  # 资金支持金额占区资金支持金额比

              # 26246,  # 企业人才服务总次数
              # get_random_num(),  # 人才服务总次数占全区人才服务次数比
              # 18123,  # 企业住房支持总次数
              # get_random_num()    # 住房支持总次数占全区住房支持次数比
            ],
            "unit": [
              "家",
              "亿",
              "%",
              "亿",
              "%",
              "万",
              "%",
              # "家",
              # "%",
              # "家",
              # "%"
            ]
          },

          "financialSupport": {
            "year": get_dict_key(thedict=data_dict, key="year"),
            "data_1": {
              "value": [
                  get_dict_key(thedict=data_dict, key="industry_fund_support", num=76561.14),
                  get_dict_key(thedict=data_dict, key="individual_tax_fund_support", num=0),
                  get_dict_key(thedict=data_dict, key="add_on_contribution_fund_support", num=0),
                  get_dict_key(thedict=data_dict, key="ysyy_fund_support", num=0),
              ],
              "name": [
                "产业资金支持",
                "个税资金支持",
                "增加值贡献奖励",
                "一事一议资金支持",
              ],
              "unit": [
                "万元",
                "万元",
                "万元",
                "万元",

              ]
            }
          },

          "PeopleServices": {
            "data_1": {
              "value": [
                  get_dict_key(thedict=data_dict, key="work_and_residence_permit"),
                  get_dict_key(thedict=data_dict, key="graduates_settlement"),
                  get_dict_key(thedict=data_dict, key="overseas_talent_service_total"),
                  get_dict_key(thedict=data_dict, key="executive_talent_total"),
              ],
              "name": [
                "工作居住办理",
                "应届生落户",
                "留学生人才引进",
                "高管人才引进"
              ],
              "unit": [
                "人",
                "人",
                "人",
                "人"
              ]
            }
          },

          "HousingProjects": {
            "data_1": {
              "value": [
                  get_dict_key(thedict=data_dict, key="czcyy_total"),
                  get_dict_key(thedict=data_dict, key="wtwjy_total"),
                  get_dict_key(thedict=data_dict, key="lyjy_total"),
                  get_dict_key(thedict=data_dict, key="rhjy_total"),
              ],
              "name": [
                "成志畅悦园",
                "梧桐湾嘉园",
                "澜悦景苑",
                "瑞辉嘉苑"
              ],
              "unit": [
                "套",
                "套",
                "套",
                "套"
              ]
            }
          },

          # 服务包企业所获资金支持与贡献区级收入变化趋势图
          "zhichi_gongxian": {
              # 年份
              "year": ["{}年".format(i) for i in five_years],
              # 区级收入
              "q_num": q_num,
              # 资金支持
              "z_num": z_num,
              "q_unit": "亿元",
              "z_unit": "万元",
          },

        }

        return static


# 1.2
class InfoHealthyView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        classify = data.get("classify", "营收")
        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        all_data = dict()
        thedict = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "select * from health_pie_chart where year={} order by year desc".format(year)
            cursor.execute(sql)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                all_data[row1["enterprise_name"]] = row1

            # sql3 = "SELECT  count(*) FROM health_pie_chart where year={} order by year desc".format(year)
            # cursor.execute(sql3)
            # rows3 = cursor.fetchall()
            total_num = len(all_data)
            total_page = int(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

            sql2 = "select * from health_pie_chart where year={} order by year desc limit 10;".format(year)
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            if len(rows2) > 0:
                thedict = rows2[0]
        if "税收" in classify:
            c3num0 = [i.get("tax_health_check_by_month") for i in list(all_data.values()) if i.get("tax_health_check_by_month")=="c3"]
            c2num0 = [i.get("tax_health_check_by_month") for i in list(all_data.values()) if i.get("tax_health_check_by_month")=="c2"]
            c1num0 = [i.get("tax_health_check_by_month") for i in list(all_data.values()) if i.get("tax_health_check_by_month")=="c1"]

            c3num1 = [i.get("tax_health_check_by_industry") for i in list(all_data.values()) if i.get("tax_health_check_by_industry") == "c3"]
            c2num1 = [i.get("tax_health_check_by_industry") for i in list(all_data.values()) if i.get("tax_health_check_by_industry") == "c2"]
            c1num1 = [i.get("tax_health_check_by_industry") for i in list(all_data.values()) if i.get("tax_health_check_by_industry") == "c1"]

            c3num2 = [i.get("tax_health_check_by_district") for i in list(all_data.values()) if i.get("tax_health_check_by_district") == "c3"]
            c2num2 = [i.get("tax_health_check_by_district") for i in list(all_data.values()) if i.get("tax_health_check_by_district") == "c2"]
            c1num2 = [i.get("tax_health_check_by_district") for i in list(all_data.values()) if i.get("tax_health_check_by_district") == "c1"]
        else:
            c3num0 = [i.get("income_health_check_by_month") for i in list(all_data.values()) if
                      i.get("income_health_check_by_month") == "c3"]
            c2num0 = [i.get("income_health_check_by_month") for i in list(all_data.values()) if
                      i.get("income_health_check_by_month") == "c2"]
            c1num0 = [i.get("income_health_check_by_month") for i in list(all_data.values()) if
                      i.get("income_health_check_by_month") == "c1"]

            c3num1 = [i.get("income_health_check_by_industry") for i in list(all_data.values()) if
                      i.get("income_health_check_by_industry") == "c3"]
            c2num1 = [i.get("income_health_check_by_industry") for i in list(all_data.values()) if
                      i.get("income_health_check_by_industry") == "c2"]
            c1num1 = [i.get("income_health_check_by_industry") for i in list(all_data.values()) if
                      i.get("income_health_check_by_industry") == "c1"]

            c3num2 = [i.get("income_health_check_by_district") for i in list(all_data.values()) if
                      i.get("income_health_check_by_district") == "c3"]
            c2num2 = [i.get("income_health_check_by_district") for i in list(all_data.values()) if
                      i.get("income_health_check_by_district") == "c2"]
            c1num2 = [i.get("income_health_check_by_district") for i in list(all_data.values()) if
                      i.get("income_health_check_by_district") == "c1"]

        # print(c3num0)
        # print(c2num0)
        # print(c1num0)
        c3num0,c2num0,c1num0,c3num1,c2num1,c1num1,c3num2,c2num2,c1num2 = len(c3num0),len(c2num0),len(c1num0),len(c3num1),len(c2num1),len(c1num1),len(c3num2),len(c2num2),len(c1num2)

        # print(c3num0,c2num0,c1num0,c3num1,c2num1,c1num1,c3num2,c2num2,c1num2)
        # print(list(all_data.values()))
        # print([page_len*(page-1),page_len*page])

        all_data = list(all_data.values())
        if "税收" in classify:
            all_data = sorted(all_data, key=lambda keys: keys["rank"])
        else:
            all_data = sorted(all_data, key=lambda keys: keys["revenue_rank"])
        # sorted(rows,key=lambda keys:keys['日期'])

        rows = all_data[page_len*(page-1):page_len*page]
            # select t.tel,count(*) from nbyd_deliver t  group   by t.tel ;


        # classify = "营收/人均营收/地均营收/税收/人均税收/地均税收/"
        # classify = data.get("classify", "营收")

        # keys = random.choice(["enterprise_tax_comparison_by_industry", "enterprise_tax_comparison", "enterprise_tax_comparison_by_region"])

        the_list = list()
        satrt = page_len*(page-1) + 1
        for row in rows:
            # n += 1
            # one = {
            #     "code": n,
            #     "name": row.get("enterprise_name"),
            #     "list1": {
            #         "value": row.get(keys, "NaN"),
            #         "color": get_random_color()
            #     }}
            if "税收" in classify:
                one = {
                        "code": get_dict_key(thedict=row, key="rank", num=satrt),
                        # "code": satrt,
                        "name": get_dict_key(thedict=row, key="enterprise_name"),
                        "list1": {
                          "value": get_dict_key(thedict=row, key="enterprise_tax_comparison", units=0.01),
                          "color": get_dict_key(thedict=row, key="tax_health_check_by_month")
                        },
                        "list2": {
                          "value": get_dict_key(thedict=row, key="enterprise_tax_comparison_by_industry", units=0.01),
                          "color": get_dict_key(thedict=row, key="tax_health_check_by_industry")
                        },
                        "list3": {
                          "value": get_dict_key(thedict=row, key="enterprise_tax_comparison_by_district", units=0.01),
                          "color": get_dict_key(thedict=row, key="tax_health_check_by_district")
                        }
                      }
            else:
                one = {
                    "code": get_dict_key(thedict=row, key="revenue_rank", num=satrt),
                    # "code": satrt,
                    "name": get_dict_key(thedict=row, key="enterprise_name"),
                    "list1": {
                        # "value": get_random_num(a=100, b=200),
                        "value": get_dict_key(thedict=row, key="enterprise_income_comparison", units=0.01),
                        "color": get_dict_key(thedict=row, key="income_health_check_by_month")
                    },

                    "list2": {
                        # "value": get_random_num(),
                        "value": get_dict_key(thedict=row, key="enterprise_income_comparison_by_industry", units=0.01),
                        "color": get_dict_key(thedict=row, key="income_health_check_by_industry")
                    },

                    "list3": {
                        # "value": get_random_num(),
                        "value": get_dict_key(thedict=row, key="enterprise_income_comparison_by_district", units=0.01),
                        "color": get_dict_key(thedict=row, key="income_health_check_by_district")
                    }
                }
            the_list.append(one)
            satrt += 1

        # print(classify)

        if "税收" in classify:
            m = 3
            show = "税收"
            cl_dict1 = {
                "red": "低于往年".format(show),       # 红
                "yellow": "与往年持平".format(show),  # 黄
                "blue": "高于往年".format(show)       # 绿
            }
            cl_dict2 = {
                "red": "同行业差异较大".format(show),  # 红
                "yellow": "与同行业存在差异".format(show),  # 黄
                "blue": "与同行业相近".format(show)  # 绿
            }
            cl_dict3 = {
                "red": "占比明显下降".format(show),  # 红
                "yellow": "占比下降".format(show),  # 黄
                "blue": "占比健康".format(show)  # 绿
            }
            try:
                m1 = round(c1num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m1 = "NaN"

            try:
                m2 = round(c2num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m2 = "NaN"

            try:
                m3 = round(c3num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m3 = "NaN"

            try:
                m11 = round(c1num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m11 = "NaN"

            try:
                m22 = round(c2num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m22 = "NaN"

            try:
                m33 = round(c3num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m33 = "NaN"

            try:
                m111 = round(c1num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m111 = "NaN"

            try:
                m222 = round(c2num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m222 = "NaN"

            try:
                m333 = round(c3num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m333 = "NaN"

            pieChart = {

                  "pie1": {
                    "value": [
                        # get_dict_key(thedict=thedict, key="", num=51),
                        # get_dict_key(thedict=thedict, key="", num=28),
                        # get_dict_key(thedict=thedict, key="", num=197)
                        # round(c3num0*100/(c3num0+c2num0+c1num0), 2),
                        m1,
                        m2,
                        m3,
                    ],
                    "color": [
                      "c1",
                      "c2",
                      "c3"
                    ],
                    # "rhl": [
                    #   a1,
                    #   a2,
                    #   a3
                    # ],
                    "speech": [
                        cl_dict1["red"],
                        cl_dict1["yellow"],
                        cl_dict1["blue"],
                    ]
                  },

                  "pie2": {
                    "value": [
                        # get_dict_key(thedict=thedict, key="", num=261),
                        # get_dict_key(thedict=thedict, key="", num=12),
                        # get_dict_key(thedict=thedict, key="", num=15)
                        m11,
                        m22,
                        m33,
                    ],
                    "color": [
                      "c1",
                      "c2",
                      "c3"
                    ],
                    # "rhl": [
                    #   b1,
                    #   b2,
                    #   b3
                    # ],
                    "speech": [
                        cl_dict2["red"],
                        cl_dict2["yellow"],
                        cl_dict2["blue"],
                    ]
                  },

                  "pie3": {
                    "value": [
                        # get_dict_key(thedict=thedict, key="", num=90),
                        # get_dict_key(thedict=thedict, key="", num=46),
                        # get_dict_key(thedict=thedict, key="", num=140)
                        m111,
                        m222,
                        m333,
                    ],
                    "color": [
                      "c1",
                      "c2",
                      "c3"
                    ],
                    # "rhl": [
                    #   c1,
                    #   c2,
                    #   c3
                    # ],
                    "speech": [
                        cl_dict3["red"],
                        cl_dict3["yellow"],
                        cl_dict3["blue"],
                    ]
                  }
                }
        else:
            show = "营收"
            m = 2

            try:
                m1 = round(c1num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m1 = "NaN"

            try:
                m2 = round(c2num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m2 = "NaN"

            try:
                m3 = round(c3num0 * 100 / (c3num0 + c2num0 + c1num0), 2)
            except:
                m3 = "NaN"

            try:
                m11 = round(c1num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m11 = "NaN"

            try:
                m22 = round(c2num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m22 = "NaN"

            try:
                m33 = round(c3num1 * 100 / (c3num1 + c2num1 + c1num1), 2)
            except:
                m33 = "NaN"

            try:
                m111 = round(c1num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m111 = "NaN"

            try:
                m222 = round(c2num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m222 = "NaN"

            try:
                m333 = round(c3num2 * 100 / (c3num2 + c2num2 + c1num2), 2)
            except:
                m333 = "NaN"
            cl_dict1 = {
                 "red": "低于往年",      # 红
                "yellow": "与往年持平",   # 黄
                "blue": "高于往年"       # 绿
            }
            cl_dict2 = {
                 "red": "低于同行业",      # 红
                "yellow": "与同行业持平",  # 黄
                "blue": "高于同行业"       # 绿
            }
            cl_dict3 = {
                "red": "占比明显下降",       # 红
                "yellow": "占比基本持平",  # 黄
                "blue": "占比明显提升"       # 绿
            }
            pieChart = {

                "pie1": {
                    "value": [
                        m1,
                        m2,
                        m3,
                    ],
                    "color": [
                        "c1",
                        "c2",
                        "c3"
                    ],
                    # "rhl": [
                    #     a1,
                    #     a2,
                    #     a3
                    # ],
                    "speech": [
                        cl_dict1["red"],
                        cl_dict1["yellow"],
                        cl_dict1["blue"],
                    ]
                },

                "pie2": {
                    "value": [
                        m11,
                        m22,
                        m33,
                    ],
                    "color": [
                        "c1",
                        "c2",
                        "c3"
                    ],
                    # "rhl": [
                    #     b1,
                    #     b2,
                    #     b3
                    # ],
                    "speech": [
                        cl_dict2["red"],
                        cl_dict2["yellow"],
                        cl_dict2["blue"],
                    ]
                },

                "pie3": {
                    "value": [
                        m111,
                        m222,
                        m333,
                    ],
                    "color": [
                        "c1",
                        "c2",
                        "c3"
                    ],
                    # "rhl": [
                    #     c1,
                    #     c2,
                    #     c3
                    # ],
                    "speech": [
                        cl_dict3["red"],
                        cl_dict3["yellow"],
                        cl_dict3["blue"],
                    ]
                }
            }

        healthy = {
              "year": year,
              "speech": "1至{}月累计{}情况".format(m, show),
              "healthlevel": {
                "type": classify,
                "speech": "1至{}月累计{}变化情况".format(m, show),

                "pieChart": pieChart,
                "list": the_list
              },
            }
        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": healthy}
        return result


# 1.3
class InfoSentimentView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        # name = data.get("name", "中国石油化工集团有限公司")
        # year = data.get("year", time.strftime('%Y', time.localtime(time.time())))

        dtime = getdate(6*30)

        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  t_articles_info where sentiment='pos' and create_time>='{}'  ORDER BY create_time desc LIMIT {} OFFSET {};".format(dtime, page_len, (page-1)*page_len)
            cursor.execute(sql)
            rows = cursor.fetchall()

            sql2 = "SELECT * FROM  t_articles_info where sentiment='neg' and create_time>='{}'  ORDER BY create_time desc LIMIT {} OFFSET {};".format(dtime, page_len, (page-1)*page_len)
            cursor.execute(sql2)
            rows2 = cursor.fetchall()

            sql3 = "SELECT count(*) FROM  t_articles_info where sentiment='pos' and create_time>='{}' ORDER BY create_time desc ;".format(dtime)
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            total_num1 = rows3[0].get("count(*)")
            total_page1 = int(total_num1 / page_len)
            if total_num1 % page_len != 0:
                total_page1 += 1

            sql4 = "SELECT count(*) FROM  t_articles_info where sentiment='neg' and create_time>='{}' ORDER BY create_time desc ;".format(
                dtime)
            cursor.execute(sql4)
            rows4 = cursor.fetchall()
            total_num2 = rows4[0].get("count(*)")
            total_page2 = int(total_num2 / page_len)
            if total_num2 % page_len != 0:
                total_page2 += 1

            if (total_num1==0) and (total_num2!=0):
                total_num = total_num2
                total_page = total_page2
            elif  (total_num2==0) and (total_num1!=0):
                total_num = total_num1
                total_page = total_page1
            else:
                if total_num1 <= total_num2:
                    total_num = total_num1
                    total_page = total_page1
                else:
                    total_num = total_num2
                    total_page = total_page2

        zheng = list()
        fu = list()

        satrt = 1+page_len*(page-1)
        for row in rows:
            t = row.get("create_time")
            try:
                t = t.strftime('%Y-%m-%d')
            except:
                pass

            zheng.append(
                {
                    "code": satrt,
                    "title": row.get("title", ""),
                    "dateTime": t,
                }
            )
            satrt += 1

        for row in rows2:
            t = row.get("create_time")
            try:
                t = t.strftime('%Y-%m-%d')
            except:
                pass
            fu.append(
                {
                    "code": satrt,
                    "title": row.get("title", ""),
                    "dateTime": t,
                }
            )
            satrt += 1


        sentiment = {
            # 正向
            "zhengxiang": zheng,
            # 负向
            "fuxiang": fu,
        }

        result = {"page": page, "page_len": page_len, "total_num": total_num,  "total_page": total_page, "data": sentiment}
        return result