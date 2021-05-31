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
    get_random_num, get_ryb, get_random_color, getdate, get_unit_num


# 2.1
class BaseinfoStaticView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))

        gaoguan = list()
        data_dict = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM screen2 WHERE enterprise_name='{}';".format(name)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                data_dict = rows[0]

            # name1 = name.replace("－", "-")
            sql2 = "SELECT * FROM screen2_dongjiangao WHERE enterprise_name='{}';".format(name)
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            for one in rows2:
                try:
                    dongjiangao_info = one["dongjiangao_info"].split("-")

                    thename = dongjiangao_info[1]

                    strss = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", thename)

                    strss = strss.replace("（", "").replace("）", "").replace(".", "")
                    strss = strss.replace("(", "").replace(")", "")
                    strss = strss.replace(" ", "")
                    if not strss:
                        strss = thename

                    two = {
                          "photo": "NaN",
                          "touxian": strss,
                          "guoji": "NaN",
                          "name": dongjiangao_info[0],
                          "education": get_dict_key(thedict=one, key="education_background_info"),
                          "major": "NaN",
                          "jian_li": get_dict_key(thedict=one, key="detail_info"),
                        }
                    gaoguan.append(two)
                except:
                    pass

        if len(gaoguan) < 3:
            for i in range(3-len(gaoguan)):
                gaoguan.append(
                    {
                        "photo": "NaN",
                        "touxian": "NaN",
                        "guoji": "NaN",
                        "name": "NaN",
                        "education": "NaN",
                        "major": "NaN",
                        "jian_li": "NaN",
                    }
                )
        if len(gaoguan) == 3:
            pass
        else:
            gaoguan = gaoguan[:3]

        # 累计营收
        v0, n0 = get_unit_num(thedict=data_dict, key="1_to_X_month_accumulate_revenue_income", unit="万")
        # 地方级收入
        v1, n1 = get_unit_num(thedict=data_dict, key="1_to_X_month_accumulate_tax_income_by_area", unit="元")
        # 区级收入
        v2, n2 = get_unit_num(thedict=data_dict, key="1_to_X_month_accumulate_tax_income_by_district", unit="元")

        static = {
          "year": year,
          "basicInfo": {

              "name": get_dict_key(thedict=data_dict, key="enterprise_name"),
              "building": get_dict_key(thedict=data_dict, key="building"),
              "industry": get_dict_key(thedict=data_dict, key="industry"),
              "peopleNum": get_dict_key(thedict=data_dict, key="employee"),
              "space": "{}m²".format(get_dict_key(thedict=data_dict, key="area")),
              "Capital": "{}".format(get_dict_key(thedict=data_dict, key="reg_capital")),
              "times": get_dict_key(thedict=data_dict, key="founded"),
              "nature": get_dict_key(thedict=data_dict, key="enterprise_nature"),
              "jie_xiang": get_dict_key(thedict=data_dict, key="townstreet"),
              "guan_jia": get_dict_key(thedict=data_dict, key="housekeeper"),
          },
          # 标签
          "enterpriseLabel": {
            "is_sjfwb_qy": 'true' if data_dict.get("city_wide_enterprise", "") else 'false',             # 市级服务包
            "is_ss_qy": 'true' if data_dict.get("listed_enterprise", "") else 'false',                   # 上市
            "is_zgcgx_qy": 'true' if data_dict.get("zhongguancun_tech_enterprise", "") else 'false',     # 中关村高新
            "is_dl_qy": 'true' if data_dict.get("degnling_plan", "") else 'false',                       # 瞪羚
            "is_qjfwb_qy": 'true' if data_dict.get("region_wide_enterprise", "") else 'false',           # 区级服务包
            "is_gs_qy": 'true' if data_dict.get("enterprise_above_designated_size", "") else 'false',    # 规上
            "is_gjzdfz_qy": 'true' if data_dict.get("jie_xiang", "") else 'false',                       # 国家重点
            "is_djs_qy": 'true' if data_dict.get("unicorn_plan", "") else 'false',                       # 独角兽
            "is_fm_qy": 'true' if data_dict.get("fengming_plan", "") else 'false',                       # 凤鸣
            "is_zb_qy": 'true' if data_dict.get("headquarter", "") else 'false',                         # 总部
            "is_kg_zb_qy": 'true' if data_dict.get("mnc_headquarter", "") else 'false',                  # 跨国总部

          },
          # 重要经济数据
          "tax": {
            "ljys_tax": {
              "number": v0,   # 累计营收
              "tb": get_dict_key(thedict=data_dict, key="ratio_change_by_revenue"),                        # 同比变化率
              "speech": "{}月至{}月累计营收".format(1, get_dict_key(thedict=data_dict, key="", num=2)),
              "unit": n0,
            },
            "dj_ljys_tax": {
              "number": v1,  # 累计地级营收
              "tb": get_dict_key(thedict=data_dict, key="ratio_change_by_area"),                      # 同比变化率
              "speech": "{}月至{}月累计地方级收入".format(1, get_dict_key(thedict=data_dict, key="", num=3)),
              "unit": n1,
            },
            "qj_ljys_tax": {
              "number": v2,      # 累计区级
              "tb": get_dict_key(thedict=data_dict, key="ratio_change_by_district"),                           # 同比变化率
              "speech": "{}月至{}月区级收入".format(1, get_dict_key(thedict=data_dict, key="", num=3)),
              "unit": n2,
            },

          },
          # 企业创新能力
          "economics": {
            "technology": {                              # 企业研发费用
              "number": get_dict_key(thedict=data_dict, key="ent_deve_cost"),
              "unit": "万"
            },
            "investment": get_dict_key(thedict=data_dict, key="ent_deve_ratio"),                # 企业研发投入比例
            "research": {
              "tb": get_dict_key(thedict=data_dict, key="ent_deve_ratio_by_year"),                      # 同比增速
              "ranking": get_dict_key(thedict=data_dict, key="ent_deve_rank")                  # 在服务包企业排名
            },
            "zj_trademark": get_dict_key(thedict=data_dict, key="trademark_obtain_in_recent_year", num=0),              # 一年商标增幅
            "zj_patent": get_dict_key(thedict=data_dict, key="patent_acquire_in_recent_year", num=0),                # 一年专利增幅
            "zj_softWork": get_dict_key(thedict=data_dict, key="computer_software_copyright _in_recent_year", num=0),               # 一年软著增幅

            "tzj_trademark": get_dict_key(thedict=data_dict, key="trademark_owned_total", num=0),  # 总商标增幅
            "tzj_patent": get_dict_key(thedict=data_dict, key="patent_owned_total", num=0),  # 总专利增幅
            "tzj_softWork": get_dict_key(thedict=data_dict, key="computer_software_copyright_owned_total", num=0)  # 总软著增幅
          },
          # 风险异动
          "riskChangeInfo": {

              "qy_change": get_dict_key(thedict=data_dict, key="enterprise_chane_in_half_year", num=0),                                # 企业变更总次数
              "djg_change": get_dict_key(thedict=data_dict, key="dongjiangao_changing_filing_increased_in_recent_half_year", num=0),   # 董监半年变更
              "faren_change": get_dict_key(thedict=data_dict, key="legal_entity_change_number", num=0),                                # 法人
              "jingying_change": get_dict_key(thedict=data_dict, key="bustiness_term_scope_change_number", num=0),                     # 经营范围
              "gq_change": get_dict_key(thedict=data_dict, key="equity_change_increased_in_recent_half_year", num=0),                  # 股权变更

              "qyfxNum": get_dict_key(thedict=data_dict, key="enterprise_risk_increment_in_recent_half_year", num=0),                     # 企业风险                  # 企业半年风险新增
              "xzcfNum": get_dict_key(thedict=data_dict, key="administrative_punishment_increased_in_recent_half_year", num=0),           # 行政处罚
              "fa_yuan_gong_gao_Num": get_dict_key(thedict=data_dict, key="court_annoucement_increment_number", num=0),                   # 法院公告
              "bei_zhi_xing": get_dict_key(thedict=data_dict, key="executed_situation_increment_number", num=0),                          # 被执行
              "sxxxNum": get_dict_key(thedict=data_dict, key="trusting_breaking_information_increased_in_recent_half_year", num=0)        # 失信信息
          },
          # 个税信息
          "ge_shui": {
              "p_num": get_dict_key(thedict=data_dict, key="award_number", num=0),
              "p_unit": "人",

              "t_num": get_dict_key(thedict=data_dict, key="total_award", num=0),
              "t_unit": "万"
          },
          # 高管信息
          "managerInfo": gaoguan,
            # [
            # {
            #   "photo": "NaN",
            #   "touxian": "NaN",
            #   "guoji": "NaN",
            #   "name": "NaN",
            #   "education": "NaN",
            #   "major": "NaN",
            #   "jian_li": "NaN",
            # },
            # {
            #   "photo": "",
            #     "touxian": "总经理",
            #     "guoji": "中国",
            #   "name": "马永生",
            #   "education": "中国工程院院士",
            #   "major": "地质学、古生物学、沉积学",
            #   "jian_li": "马永生，男，汉族，1961年9月生，内蒙古土默特左旗人，1984年马永生从武汉地质学院地质系毕业，1987年获得中国地质大学研究生院地质系理学硕士学位，1994年11月加入中国共产党，沉积学家，石油地质学家，石油与天然气勘探专家，中国工程院院士。",
            # },
            # {
            #   "photo": "",
            #     "touxian": "董事会主席",
            #     "guoji": "中国",
            #   "name": "熊维平",
            #   "education": "中国工程院院士",
            #   "major": "选矿专业",
            #   "jian_li": "熊维平，男，汉族，1956年11月生，江西南昌人，1971年9月参加工作，1976年6月加入中国共产党，江西冶金学院（现江西理工大学）矿业系选矿专业毕业，研究生学历，工学博士学位，博士后，教授，北京大学博士生导师。",
            # }

          # ]
        }

        return static


# 2.2
class BaseinfoSentimentView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        # 迁入/迁出，并购，高管，处罚，正面，负面
        if page == 0:
            page = 1

        dtime = getdate(6 * 30)

        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  t_articles_info WHERE companies LIKE '{}%'  and create_time>='{}'  ORDER BY create_time desc LIMIT {} OFFSET {};".format(
                name, dtime, page_len, (page-1)*page_len)
            # print(sql)

            cursor.execute(sql)
            rows = cursor.fetchall()

            sql3 = "SELECT count(*) FROM  t_articles_info WHERE companies LIKE '{}%'  and create_time>='{}'  ORDER BY create_time desc".format(name, dtime)
            # print(sql3)

            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            total_num = rows3[0].get("count(*)")
            total_page = math.floor(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

        sentiment = list()
        satrt = 1 + page_len * (page - 1)
        for row in rows:
            t = row.get("create_time")
            try:
                t = t.strftime('%Y-%m-%d')
            except:
                pass

            sentiment.append(
                {
                    "code": satrt,
                    "title": row.get("title", ""),
                    "dateTime": t,
                    "url": row.get("url", ""),
                    "brief": row.get("brief", ""),
                })
            satrt += 1

        # 本企业
        # sentiment = list()
        # for i in range(1+page_len*(page-1), 1+page_len*page):
        #     sentiment.append(
        #             {
        #                 "code": i,
        #                 "title": "阿里云-{}".format(i),
        #                 "dateTime": "2020/2/1 11:26:00"
        #             })

        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": sentiment}
        return result
