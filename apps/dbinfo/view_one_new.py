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
    get_random_num, get_ryb, get_random_color, getdate, get_unit_value


# 1,模块static
class InfoStaticView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))

        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        year_data = dict()
        five_years = [i for i in range(year-5, year)]
        all_data = dict()
        # data_dict = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "select * from screen1 where year<={} order by year desc;".format(year)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                year_data = rows[0]
            for one in rows:
                all_data[one["year"]] = one

        # q_num = [get_dict_key(thedict=all_data.get(i, {}), key="district_tax_income", units=10000*10000) for i in five_years]
        # z_num = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund") for i in five_years]
        q_num = [get_dict_key(thedict=all_data.get(i, {}), key="dstr_tax_incm", units=10000*10000) for i in five_years]
        z_num = [get_dict_key(thedict=all_data.get(i, {}), key="support_fund") for i in five_years]
        z_num[-1] = z_num[-2]

        m = 2
        shuim = 4

        v1 = sum([get_dict_key(thedict=v, key="industry_fund_support", num=0) for k, v in all_data.items()])
        v2 = sum([get_dict_key(thedict=v, key="individual_tax_fund_support", num=0) for k, v in all_data.items()])
        v3 = sum([get_dict_key(thedict=v, key="add_on_contribution_fund_support", num=0) for k, v in all_data.items()])
        v4 = sum([get_dict_key(thedict=v, key="ysyy_fund_support", num=0) for k, v in all_data.items()])

        a1, n1 = get_unit_value(value=v1, unit="万")
        a2, n2 = get_unit_value(value=v2, unit="万")
        a3, n3 = get_unit_value(value=v3, unit="万")
        a4, n4 = get_unit_value(value=v4, unit="万")

        static = {
          # 模块1， 朝阳区服务包企业基本信息
          "EnterpriseInfo": {
            "year": year-1,
            "speech": "当年1至{}月累计".format(shuim),
            "number": [
              get_dict_key(thedict=year_data, key="enterprise_number"),  # 企业数量
              get_dict_key(thedict=year_data, key="local_tax_income", units=10000*10000),  # 地方级收入总量
              get_dict_key(thedict=year_data, key="local_tax_income_by_district_rate"),  # 地方级收入占全区地方级收入比
              # get_dict_key(thedict=data_dict, key="district_tax_income", units=10000*10000),  # 企业区级收入总量
              # get_dict_key(thedict=data_dict, key="district_tax_income_by_district_rate"),  # 区级收入占全区区级收入比
              get_dict_key(thedict=all_data.get(2020, {}), key="support_fund"),                          # 企业资金支持金额总量
              get_dict_key(thedict=all_data.get(2020, {}), key="support_fund_by_district_rate", units=0.01),  # 资金支持金额占区资金支持金额比

              # 26246,  # 企业人才服务总次数
              # get_random_num(),  # 人才服务总次数占全区人才服务次数比
              # 18123,  # 企业住房支持总次数
              # get_random_num()    # 住房支持总次数占全区住房支持次数比
            ],
            "unit": [
              "家",
              "亿",
              "%",
              # "亿",
              # "%",
              "万",
              "%",
              # "家",
              # "%",
              # "家",
              # "%"
            ]
          },

          # 模块5
          "financialSupport": {
            "year": get_dict_key(thedict=year_data, key="year"),
            "data_1": {
              "value": [
                  a1,
                  a2,
                  a3,
                  a4,
                  # sum([get_dict_key(thedict=v, key="industry_fund_support", num=0) for k, v in all_data.items()]),
                  # sum([get_dict_key(thedict=v, key="individual_tax_fund_support", num=0) for k, v in all_data.items()]),
                  # sum([get_dict_key(thedict=v, key="add_on_contribution_fund_support", num=0) for k, v in all_data.items()]),
                  # sum([get_dict_key(thedict=v, key="ysyy_fund_support", num=0) for k, v in all_data.items()]),
                  #
                  #
                  # get_dict_key(thedict=year_data, key="individual_tax_fund_support", num=0),
                  # get_dict_key(thedict=year_data, key="add_on_contribution_fund_support", num=0),
                  # get_dict_key(thedict=year_data, key="ysyy_fund_support", num=0),
              ],
              "name": [
                "产业资金支持",
                "个税资金支持",
                "增加值贡献奖励",
                "一事一议资金支持",
              ],
              "unit": [
                  n1,
                  n2,
                  n3,
                  n4,
                # "万元",
                # "万元",
                # "万元",
                # "万元",

              ]
            }
          },

          "PeopleServices": {
            "data_1": {
              "value": [
                  sum([get_dict_key(thedict=v, key="work_and_residence_permit", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="graduates_settlement", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="overseas_talent_service_total", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="executive_talent_total", num=0) for k, v in all_data.items()]),

                  # get_dict_key(thedict=year_data, key="work_and_residence_permit"),
                  # get_dict_key(thedict=year_data, key="graduates_settlement"),
                  # get_dict_key(thedict=year_data, key="overseas_talent_service_total"),
                  # get_dict_key(thedict=year_data, key="executive_talent_total"),
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
                  sum([get_dict_key(thedict=v, key="czcyy_total", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="wtwjy_total", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="lyjy_total", num=0) for k, v in all_data.items()]),
                  sum([get_dict_key(thedict=v, key="rhjy_total", num=0) for k, v in all_data.items()]),

                  # get_dict_key(thedict=year_data, key="czcyy_total"),
                  # get_dict_key(thedict=year_data, key="wtwjy_total"),
                  # get_dict_key(thedict=year_data, key="lyjy_total"),
                  # get_dict_key(thedict=year_data, key="rhjy_total"),
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

          # 营收
          "ying_shou": {
            "number": get_dict_key(thedict=year_data, key="total_reve_incm", units=10000*10000),
            "unit": "亿元",
            "zeng_su": get_dict_key(thedict=year_data, key="total_reve_change_ratio"),
            "speech": "1至{}月累计营收情况".format(m),
          },
          # 税收
          "shui_shou": {
                "number": get_dict_key(thedict=year_data, key="dstr_tax_incm", units=10000*10000),
                "unit": "亿元",
                "zeng_su": get_dict_key(thedict=year_data, key="dstr_tax_incm_change_rate"),
                "speech": "1至{}月累计税收情况".format(4),
          },
          # 利润
          "lirun": {
                "number": get_dict_key(thedict=year_data, key="total_profit", units=10000*10000),
                "unit": "亿元",
                "zeng_su": get_dict_key(thedict=year_data, key="total_profit_change_ratio"),
                "speech": "1至{}月累计利润情况".format(m),
          },

        # 人地均
        "ren_di": {
             "ren_number": get_dict_key(thedict=year_data, key="ent_dstr_tax_incm_by_emp", units=10000),
             "ren_unit": "万元/人",
             "di_number": get_dict_key(thedict=year_data, key="ent_dstr_tax_incm_by_area", units=10000),
             "di_unit": "万元/平米",
             "speech": "1至{}月累计人地均区级收入情况".format(4),
        },

        }

        return static


# 1,模块pic
class Picshow(BaseView):

    def get(self, request):
        data = request.GET.copy()

        classify = data.get("classify", "营收")
        # year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        # year = int(year)
        timedata = dict()
        all_data = dict()
        attr_dict = {
            "营收": "income_health_check_by_month",
            "营收行业": "income_health_check_by_industry",
            "税收": "tax_health_check_by_month",
            "税收行业": "tax_health_check_by_industry",
            "利润": "profit_health_check",
            "利润增速": "profit_by_industry_health_check",
            "人均": "tax_by_emp_health_check",
            "地均": "tax_by_area_health_check",

        }
        key = attr_dict.get(classify, "")

        with MysqlDB(database=RPDSQL) as cursor:
            sql1 = "select year,month from health_pie_chart;"
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                timedata[row1["year"]] = timedata.get(row1["year"], [])
                timedata[row1["year"]].append(row1["month"])

            year = max(list(timedata.keys()))
            month = max(timedata[year])

            sql = "select * from health_pie_chart where year={} and month={};".format(year, month)
            # print(classify, sql)

            cursor.execute(sql)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                all_data[row1["enterprise_name"]] = row1
        c1num0 = [i.get(key) for i in list(all_data.values()) if i.get(key) == "c1"]
        c2num0 = [i.get(key) for i in list(all_data.values()) if i.get(key) == "c2"]
        c3num0 = [i.get(key) for i in list(all_data.values()) if i.get(key) == "c3"]

        # print(c3num0)
        # print(c2num0)
        # print(c1num0)
        # c3num0 = len(c3num0)
        # c2num0 = len(c2num0)
        # c1num0 = len(c1num0)
        # c3num0, c2num0, c1num0 = len(c3num0), len(c2num0), len(c1num0)
        # if classify == "营收行业":
        #     pass
        # else:
        #     speech = ["同比变化>3%", "同比变化±3%", "同比变化<-3%"]
        speech = ["同比下降", "同比持平", "同比增长"]

        healthy = {
            "year": year,
            "classify": classify,
            "pic_data": {
                "color": ["c1", "c2", "c3"],
                "number": [len(c1num0), len(c2num0), len(c3num0)],
                "speech": speech,
                "unit": "家",
            },

            }
        return healthy


# 1.1 营收
class InfoStaticOneView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        classify = data.get("classify", "营收增速")
        # 营收同比增长、营收同比持平，营收同比下降， 增速超同行、增速持平同行、增速低于同行
        all_data = dict()
        timedata = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql1 = "select year,month from health_pie_chart;"
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                timedata[row1["year"]] = timedata.get(row1["year"], [])
                timedata[row1["year"]].append(row1["month"])

            year = max(list(timedata.keys()))
            month = max(timedata[year])

            sql = "select * from health_pie_chart where year={} and month={};".format(year, month)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                all_data[row["enterprise_name"]] = row

            # total_num = len(all_data)
            # total_page = int(total_num / page_len)
            # if total_num % page_len != 0:
            #     total_page += 1

        # all_data = list(all_data.values())
        # key_dict = {
        #     "营收同比增长": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        #     "营收同比持平": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        #     "营收同比下降": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        #     "增速超同行": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        #     "增速持平同行": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        #     "增速低于同行": {"sorted_key": "", "value_key": "", "color_key": "", "desc": "desc"},
        # }
        #
        # sorted_key = key_dict.get(classify, {}).get("sorted_key", "")
        # value_key = key_dict.get(classify, {}).get("value_key", "")
        # color_key = key_dict.get(classify, {}).get("color_key", "")
        # desc_key = key_dict.get(classify, {}).get("desc", "")
        #
        # all_data = sorted(all_data, key=lambda keys: keys[sorted_key])
        # datas = all_data[page_len * (page - 1):page_len * page]

        # the_list = list()
        # satrt = page_len * (page - 1) + 1
        # for onedata in datas:
        #
        #     one = {
        #         "code": get_dict_key(thedict=onedata, key="rank", num=satrt),
        #         "name": get_dict_key(thedict=onedata, key="enterprise_name"),
        #         "value": get_dict_key(thedict=onedata, key=value_key, units=0.01),
        #         "color": get_dict_key(thedict=onedata, key=color_key)
        #     }
        #     the_list.append(one)
        #     satrt += 1

        healthy = {
            "year": year,
            # "data_list": the_list,
            "ying_shou_tong_bi": {
                "number": [
                    self.get_key_num(all_data=all_data, key="income_health_check_by_month", color="c3"),
                    self.get_key_num(all_data=all_data, key="income_health_check_by_month", color="c2"),
                    self.get_key_num(all_data=all_data, key="income_health_check_by_month", color="c1"),
                    self.get_key_num_big(all_data=all_data, key="enterprise_income_comparison", color=10),
                    self.get_key_num_small(all_data=all_data, key="enterprise_income_comparison", color=-10),
                ],
                "unit": [
                    "家",
                    "家",
                    "家",
                    "家",
                    "家",
                ],
                "speech": [
                    "同比增长企业数量",
                    "同比持平企业数量",
                    "同比下降企业数量",
                    "营收同比显著增长企业数量",
                    "营收同比显著下降企业数量",
                ],
            },

            "ying_shou_zeng_su": {
                "number": [
                    self.get_key_num(all_data=all_data, key="income_health_check_by_industry", color="c3"),
                    self.get_key_num(all_data=all_data, key="income_health_check_by_industry", color="c2"),
                    self.get_key_num(all_data=all_data, key="income_health_check_by_industry", color="c1"),
                    self.get_key_num_big(all_data=all_data, key="enterprise_income_comparison_by_industry", color=10),
                    self.get_key_num_small(all_data=all_data, key="enterprise_income_comparison_by_industry", color=-10),
                ],
                "unit": [
                    "家",
                    "家",
                    "家",
                    "家",
                    "家",
                ],
                "speech": [
                    "增速超同行业企业数量",
                    "增速与同行业持平企业数量",
                    "增速低于同行业企业数量",
                    "营收增速显著高于同行业企业数量",
                    "营收增速显著低于同行业企业数量",
                ],
            },

        }
        # result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": healthy}
        return healthy


# 1.1营收饼图列表， 1.2 税收饼图列表
class InfoStaticOneListView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        classify = data.get("classify", "")
        # 营收同比增长、营收同比持平，营收同比下降， 增速超同行、增速持平同行、增速低于同行
        all_data = dict()
        timedata = dict()

        key_dict = {
            "营收同比增长": {"cv": "c3", "color_v": "income_health_check_by_month", "sorted_key": "enterprise_income_comparison",
                       "value_key": "income_health_check_by_month", "color_key": "c3", "desc": True},
            "营收同比持平": {"cv": "c2", "color_v": "income_health_check_by_month", "sorted_key": "enterprise_income_comparison",
                       "value_key": "income_health_check_by_month", "color_key": "c2", "desc": True},
            "营收同比下降": {"cv": "c1", "color_v": "income_health_check_by_month", "sorted_key": "enterprise_income_comparison",
                       "value_key": "income_health_check_by_month", "color_key": "c1", "desc": False},

            "增速超同行": {"cv": "c3", "color_v": "income_health_check_by_industry",
                      "sorted_key": "enterprise_income_comparison_by_industry",
                      "value_key": "income_health_check_by_industry", "color_key": "c3", "desc": True},
            "增速持平同行": {"cv": "c2", "color_v": "income_health_check_by_industry",
                       "sorted_key": "enterprise_income_comparison_by_industry",
                       "value_key": "income_health_check_by_industry", "color_key": "c2", "desc": True},
            "增速低于同行": {"cv": "c1", "color_v": "income_health_check_by_industry",
                       "sorted_key": "enterprise_income_comparison_by_industry",
                       "value_key": "income_health_check_by_industry", "color_key": "c1", "desc": False},

            "税收同比增长": {"cv": "c3", "color_v": "tax_health_check_by_month", "sorted_key": "enterprise_tax_comparison",
                       "value_key": "tax_health_check_by_month", "color_key": "c3", "desc": True},
            "税收同比持平": {"cv": "c2", "color_v": "tax_health_check_by_month", "sorted_key": "enterprise_tax_comparison",
                       "value_key": "tax_health_check_by_month", "color_key": "c2", "desc": True},
            "税收同比下降": {"cv": "c1", "color_v": "tax_health_check_by_month", "sorted_key": "enterprise_tax_comparison",
                       "value_key": "tax_health_check_by_month", "color_key": "c1", "desc": False},

            "税收增速超同行": {"cv": "c3", "color_v": "tax_health_check_by_industry",
                        "sorted_key": "enterprise_tax_comparison_by_industry",
                        "value_key": "tax_health_check_by_industry", "color_key": "c3", "desc": True},
            "税收增速持平同行": {"cv": "c2", "color_v": "tax_health_check_by_industry",
                         "sorted_key": "enterprise_tax_comparison_by_industry",
                         "value_key": "tax_health_check_by_industry", "color_key": "c2", "desc": True},
            "税收增速低于同行": {"cv": "c1", "color_v": "tax_health_check_by_industry",
                         "sorted_key": "enterprise_tax_comparison_by_industry",
                         "value_key": "tax_health_check_by_industry", "color_key": "c1", "desc": False},

        }

        sorted_key = key_dict.get(classify, {}).get("sorted_key", "enterprise_income_comparison")
        # value_key = key_dict.get(classify, {}).get("value_key", "")
        # color_key = key_dict.get(classify, {}).get("color_key", "NaN")
        color_v = key_dict.get(classify, {}).get("color_v", "income_health_check_by_month")
        cv = key_dict.get(classify, {}).get("cv", "c1")
        desc_key = key_dict.get(classify, {}).get("desc", True)

        with MysqlDB(database=RPDSQL) as cursor:
            sql1 = "select year,month from health_pie_chart;"
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                timedata[row1["year"]] = timedata.get(row1["year"], [])
                timedata[row1["year"]].append(row1["month"])

            year = max(list(timedata.keys()))
            month = max(timedata[year])

            sql = "select * from health_pie_chart where year={} and month={} and {}='{}' order by {}".format(year, month, color_v, cv, sorted_key)
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                all_data[row["enterprise_name"]] = row

            total_num = len(all_data)
            total_page = int(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

        all_data = list(all_data.values())
        hangye = dict()
        for onecdata in all_data:
            h = onecdata.get("business_type", "")
            hangye[h] = hangye.get(h, 0)
            hangye[h] += 1

        # if "其他行业" in hangye:
        #     del hangye["其他行业"]

        hangye = [{"name": k, "value": v, "unit": "家"} for k, v in hangye.items()]
        hangye = sorted(hangye, key=lambda keys: keys["value"], reverse=True)
        if len(hangye) > 5:
            hangye = hangye[:5]
        elif len(hangye) < 5:
            for i in range(5-len(hangye)):
                hangye.append({"name": "无行业", "value": 0, "unit": "家"})

        h1 = list()
        h2 = list()
        h3 = list()
        for one in hangye:
            h1.append(one["name"])
            h2.append(one["value"])
            h3.append(one["unit"])

        all_data1 = [i for i in all_data if int(i.get(sorted_key)) != 9999999999]
        all_data2 = [i for i in all_data if int(i.get(sorted_key)) == 9999999999]

        all_data1 = sorted(all_data1, key=lambda keys: keys[sorted_key], reverse=desc_key)
        all_data = all_data1 + all_data2
        datas = all_data[page_len * (page - 1):page_len * page]
        the_list = list()
        satrt = page_len * (page - 1) + 1
        for onedataone in datas:
            # print(sorted_key, get_dict_key(thedict=onedataone, key="enterprise_name"), onedataone)

            one = {
                "code": satrt,
                "name": get_dict_key(thedict=onedataone, key="enterprise_name"),
                "value": "{}%".format(get_dict_key(thedict=onedataone, key=sorted_key)),
                "color": cv,
            }
            the_list.append(one)
            satrt += 1

        healthy = {
            "year": year,
            "classify": classify,
            "pic": {
                "hangye": h1,
                "number": h2,
                "unit": h3,
            },
            "data_list": the_list,
        }
        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": healthy}
        return result


# 1.2税收
class InfoStaticTwoView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        classify = data.get("classify", "营收增速")
        # 营收同比增长、营收同比持平，营收同比下降， 增速超同行、增速持平同行、增速低于同行
        all_data = dict()
        timedata = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql1 = "select year,month from health_pie_chart;"
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            for row1 in rows1:
                timedata[row1["year"]] = timedata.get(row1["year"], [])
                timedata[row1["year"]].append(row1["month"])

            year = max(list(timedata.keys()))
            month = max(timedata[year])

            sql = "select * from health_pie_chart where year={} and month={};".format(year, month)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                all_data[row["enterprise_name"]] = row

        healthy = {
            "year": year,
            "shui_shou_tong_bi": {
                "number": [
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_month", color="c3"),
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_month", color="c2"),
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_month", color="c1"),
                    self.get_key_num_big(all_data=all_data, key="enterprise_tax_comparison", color=10),
                    self.get_key_num_small(all_data=all_data, key="enterprise_tax_comparison", color=-10),
                ],
                "unit": [
                    "家",
                    "家",
                    "家",
                    "家",
                    "家",
                ],
                "speech": [
                    "同比增长",
                    "同比持平",
                    "同比下降",
                    "税收同比显著增长",
                    "税收同比显著下降",
                ],
            },

            "shui_shou_zeng_su": {
                "number": [
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_industry", color="c3"),
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_industry", color="c2"),
                    self.get_key_num(all_data=all_data, key="tax_health_check_by_industry", color="c1"),
                    self.get_key_num_big(all_data=all_data, key="enterprise_tax_comparison_by_industry", color=10),
                    self.get_key_num_small(all_data=all_data, key="enterprise_tax_comparison_by_industry", color=-10),
                ],
                "unit": [
                    "家",
                    "家",
                    "家",
                    "家",
                    "家",
                ],
                "speech": [
                    "增速超同行业",
                    "增速与同行业持平",
                    "增速低于同行业",
                    "税收增速显著高于同行业",
                    "税收增速显著低于同行业",
                ],
            },

        }
        return healthy


# 1.3 服务包企业政府支持
class InfoStaticThreeView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        all_data = dict()
        year_data = dict()
        bingtu = dict()
        five_year = list()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  s1_3_top_middle  ORDER BY year desc LIMIT 1 OFFSET 0;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            year = rows[0].get("year", year)
            five_year = [i for i in range(year-4, year+1)]

            sql2 = "SELECT * FROM  s1_3_top_middle ORDER BY year desc;"
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            if len(rows2) > 0:
                year_data = rows2[0]

            for row2 in rows2:
                all_data[row2["year"]] = row2

            sql3 = "SELECT * FROM  s1_3_indus_dist order by proportion_ranking;"
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            for row3 in rows3:
                support_category = row3["support_category"]
                industry_category = row3["industry_category"]
                proportion_num = row3["proportion_num"]
                proportion_ranking = row3["proportion_ranking"]
                bingtu[support_category] = bingtu.get(support_category, [[], [], []])
                bingtu[support_category][0].append(industry_category)
                bingtu[support_category][1].append(proportion_num)
                bingtu[support_category][2].append(proportion_ranking)

        z1 = [
            [
                get_dict_key(thedict=all_data.get(i, {}), key="support_fund"),
                get_dict_key(thedict=all_data.get(i, {}), key="industrial_support_fund"),
                get_dict_key(thedict=all_data.get(i, {}), key="individual_tax_support_fund"),
                get_dict_key(thedict=all_data.get(i, {}), key="ysyy_support_fund"),
                get_dict_key(thedict=all_data.get(i, {}), key="add_on_contribution_fund_support"),

             ] for i in five_year
        ]

        r1 = [get_dict_key(thedict=all_data.get(i, {}), key="talent_service") for i in five_year]
        f1 = [get_dict_key(thedict=all_data.get(i, {}), key="housing_support") for i in five_year]

        healthy = {

            # 资金支持
            "zi_jin_zhi_chi": {
                "qi_ye_shu_liang": get_dict_key(thedict=year_data, key="support_fund_enterprise_num"),
                "zhan_bi": get_dict_key(thedict=year_data, key="support_fund_enterprise_per"),
                "unit": "家",
                "pic": {
                    "classify": "资金",
                    "hang_ye": bingtu.get("资金", [[], [], []])[0],
                    "number": bingtu.get("资金", [[], [], []])[1],
                    "rank": bingtu.get("资金", [[], [], []])[2],
                },
                "five_year": {
                    "year": ["{}年".format(i) for i in five_year],
                    "speech": ["资金支持", "产业资金支持", "个税资金支持", "一事一议资金奖励", "增加至贡献奖励"],
                    "number": z1,
                    "unit": "万元",

                },

            },
            # 人才服务
            "ren_cai_fu_wu": {
                "qi_ye_shu_liang": get_dict_key(thedict=year_data, key="talent_service_enterprise_num"),
                "zhan_bi": get_dict_key(thedict=year_data, key="talent_service_enterprise_per"),
                "unit": "家",
                "pic": {
                    "classify": "人才",
                    "hang_ye": bingtu.get("人才", [[], [], []])[0],
                    "number": bingtu.get("人才", [[], [], []])[1],
                    "rank": bingtu.get("人才", [[], [], []])[2],

                },
                "five_year": {
                    "year": ["{}年".format(i) for i in five_year],
                    "number": r1,
                    "unit": "次",
                },
            },
            # 住房支持
            "zhu_fang_zhi_chi": {
                "qi_ye_shu_liang": get_dict_key(thedict=year_data, key="housing_support_enterprise_num"),
                "zhan_bi": get_dict_key(thedict=year_data, key="housing_support_enterprise_per"),
                "unit": "家",
                "pic": {
                    "classify": "住房",
                    "hang_ye": bingtu.get("住房", [[], [], []])[0],
                    "number": bingtu.get("住房", [[], [], []])[1],
                    "rank": bingtu.get("住房", [[], [], []])[2],

                },
                "five_year": {
                    "year": ["{}年".format(i) for i in five_year],
                    "number": f1,
                    "unit": "次",
                },
            },

            }
        return healthy


# 1.3 支持排名情况
class InfoRankView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        classify = data.get("classify", "资金")
        # 资金，人才，住房
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        rank_dict = {
            "资金": {"rank_key": "support_fund_rank", "value_key": "support_fund", "unit": "万"},
            "人才": {"rank_key": "talent_service_rank", "value_key": "talent_service", "unit": "次"},
            "住房": {"rank_key": "housing_support_rank", "value_key": "housing_support", "unit": "次"},
        }
        rank_key = rank_dict.get(classify, {}).get("rank_key", "support_fund_rank")
        value_key = rank_dict.get(classify, {}).get("value_key", "support_fund")
        unit = rank_dict.get(classify, {}).get("unit", "万")

        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  s1_3_bottom  ORDER BY year desc LIMIT 1 OFFSET 0;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            year = rows[0].get("year", year)

            sql2 = "SELECT * FROM  s1_3_bottom where year='{}' ORDER BY {} LIMIT {} OFFSET {};".format(year, rank_key, page_len, (page-1)*page_len)
            cursor.execute(sql2)
            rows2 = cursor.fetchall()

            sql3 = "SELECT count(*) FROM  s1_3_bottom where year='{}';".format(year)
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            total_num = rows3[0].get("count(*)")
            total_page = int(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

        the_list = list()
        for row2 in rows2:

            the_list.append(
                {
                    "code": get_dict_key(thedict=row2, key=rank_key),
                    "name": get_dict_key(thedict=row2, key="enterprise_name"),
                    "number": get_dict_key(thedict=row2, key=value_key, num=0),
                    "unit": unit,
                }
            )

        data = {"year": year, "classify": classify, "data_list": the_list}
        result = {"page": page, "page_len": page_len, "total_num": total_num,  "total_page": total_page, "data": data}
        return result
