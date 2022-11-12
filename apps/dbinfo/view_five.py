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


# 5.1
class StockRightView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year) - 1
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 5))
        # 投资/注资
        classify = data.get("classify", "")

        static = {
            # 企业名称
            "name": name,
            "classify": classify,
            "infolist": [
            ],
        }
        # print(classify)
        if classify == "注资":
            tb = "screen5_fund_injection_ent_list"

            with MysqlDB(database=RPDSQL) as cursor:
                sql = "SELECT * FROM  {} WHERE name='{}' order by equity desc LIMIT {} OFFSET {};".format(tb, name,page_len, (page - 1) * page_len)
                # print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()

                sql3 = "SELECT count(*) FROM {} WHERE name='{}' order by equity desc;".format(tb, name)
                cursor.execute(sql3)
                rows3 = cursor.fetchall()
                total_num = rows3[0].get("count(*)")
                total_page = int(total_num / page_len)
                if total_num % page_len != 0:
                    total_page += 1

                satrt = 1 + page_len * (page - 1)
                for row in rows:
                    try:
                        amount = get_dict_key(thedict=row, key="amount")
                        if amount > 10000:
                            amount = round(amount / 10000, 2)
                            amount = "{}亿元".format(amount)
                        else:
                            amount = "{}万元".format(amount)
                    except:
                        amount = "NaN"

                    static["infolist"].append(
                        {
                            "code": satrt,
                            "time": "NaN",
                            "equity": "{}%".format(get_dict_key(thedict=row, key="equity", units=0.01)),
                            "invested_name": get_dict_key(thedict=row, key="invested_name"),
                            "money": amount,
                            # "proportion": get_random_num()
                        }
                    )
                    satrt += 1
        elif classify == "投资":
            tb = "screen5_invest_ent_list"
            with MysqlDB(database=RPDSQL) as cursor:
                sql = "SELECT * FROM  {} WHERE name='{}' order by gubi desc LIMIT {} OFFSET {};".format(tb, name,page_len, (page - 1) * page_len)

                # print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()

                sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  order by gubi desc;".format(tb, name)

                cursor.execute(sql3)
                rows3 = cursor.fetchall()
                total_num = rows3[0].get("count(*)")
                total_page = int(total_num / page_len)
                if total_num % page_len != 0:
                    total_page += 1

                satrt = 1 + page_len * (page - 1)
                for row in rows:
                    static["infolist"].append(
                        {
                            "code": satrt,
                            "time": "NaN",
                            "equity": "{}%".format(get_dict_key(thedict=row, key="gubi", units=0.01)),
                            "invested_name": get_dict_key(thedict=row, key="gudong_name"),
                            "money": get_dict_key(thedict=row, key="gudong_renjiao"),
                            # "proportion": get_random_num()
                        }
                    )
                    satrt += 1

        else:
            tb = "screen5_invest_ent_list"
            total_num = 0
            total_page = 0

        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": static}
        return result


# 5.2
class ChangeInfoView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year) - 1
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 5))
        # 董监/法人/经营/股权
        classify = data.get("classify", "董监")
        # path = os.path.join(JSONDATA_PATH, "enterprises_baseinfo", "static.json")
        # with open(path, "r") as rf:

        static = {
            # 企业名称
            "name": name,
            "classify": classify,
            "number": 0,
            "infolist": [
            ],
        }

        dtime = getdate(6 * 30)

        # print(classify)
        if classify == "董监":
            tb = "screen5_dongjiangao_change"
        elif classify == "法人":
            tb = "screen5_legal_person_change"
        elif classify == "经营":
            tb = "screen5_business_scope_change"
        elif classify == "股权":
            tb = "screen5_equity_change"
        else:
            tb = ""
            total_num = 0
            total_page = 0

        if tb != "":
            with MysqlDB(database=RPDSQL) as cursor:
                sql = "SELECT * FROM  {} WHERE name='{}' and change_date>={} order by change_date LIMIT {} OFFSET {};".format(
                    tb, name, dtime, page_len, (page - 1) * page_len)
                # print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()

                sql3 = "SELECT count(*) FROM  {} WHERE name='{}' and change_date>={} order by change_date;".format(tb,
                                                                                                                   name,
                                                                                                                   dtime)

                cursor.execute(sql3)
                rows3 = cursor.fetchall()
                total_num = rows3[0].get("count(*)")
                total_page = int(total_num / page_len)
                if total_num % page_len != 0:
                    total_page += 1

                satrt = 1 + page_len * (page - 1)
                thelist = list()
                for row in rows:
                    thelist.append(
                        {
                            "code": satrt,
                            "after_content": get_dict_key(thedict=row, key="after_content"),
                            "before_content": get_dict_key(thedict=row, key="before_content"),
                            "change_item": get_dict_key(thedict=row, key="change_item"),
                            "change_date": get_dict_key(thedict=row, key="change_date"),

                        }
                    )
                satrt += 1

            static["infolist"] = thelist
            static["number"] = total_num
        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": static}
        return result


# 5.3
class RiskInfoView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year) - 1
        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 5))
        # 被执行/法院公告/行政处罚/裁判文书/开庭公告/经营异常/司法冻结/失信信息
        classify = data.get("classify", "")
        # path = os.path.join(JSONDATA_PATH, "enterprises_baseinfo", "static.json")
        # with open(path, "r") as rf:
        classify_dict = {
            "行政处罚": "screen5_adm_penalty",
            "法院公告": "screen5_court_notice",
            "开庭公告": "screen5_court_session_notice",
            "失信信息": "screen5_default",
            "被执行": "screen5_ent_by_execution",
            "裁判文书": "screen5_judge_doc",
            "司法冻结": "screen5_judicial_freezing",
        }
        tb = classify_dict.get(classify, "")

        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=-6 * 30)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y/%m/%d')

        static = {
            # 企业名称
            "name": name,
            "classify": classify,
            "number": 0,
            "infolist": [
            ],
        }
        satrt = 1 + page_len * (page - 1)
        if tb != "":
            with MysqlDB(database=RPDSQL) as cursor:
                if classify == "行政处罚":
                    sql = "SELECT * FROM  {} WHERE name='{}' and date>='{}' order by date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and date>='{}' order by date ;".format(tb, name,
                                                                                                             re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                # "number": get_dict_key(thedict=row, key="number"),
                                "time": get_dict_key(thedict=row, key="date"),
                                # "push_type_one": get_dict_key(thedict=row, key="push_type_one"),
                                # "push_type_two": get_dict_key(thedict=row, key="push_type_two"),
                                "title": get_dict_key(thedict=row, key="reason"),
                                "brief": get_dict_key(thedict=row, key="content"),
                            }
                        )
                        satrt += 1
                elif classify == "法院公告":
                    sql = "SELECT * FROM  {} WHERE name='{}' and date>='{}' order by date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and date>='{}' order by date ;".format(tb, name,
                                                                                                             re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                # "type": get_dict_key(thedict=row, key="type"),
                                "time": get_dict_key(thedict=row, key="date"),
                                # "role": get_dict_key(thedict=row, key="role"),
                                # "url": get_dict_key(thedict=row, key="url"),
                                "title": get_dict_key(thedict=row, key="content"),
                                "brief": get_dict_key(thedict=row, key="content"),

                            }
                        )
                        satrt += 1
                elif classify == "开庭公告":
                    re_date = (today + offset).strftime('%Y-%m-%d')
                    sql = "SELECT * FROM  {} WHERE name='{}' and hearing_date>='{}' order by hearing_date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and hearing_date>='{}' order by hearing_date ;".format(
                        tb, name,
                        re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                "title": get_dict_key(thedict=row, key="case_reason"),
                                "time": get_dict_key(thedict=row, key="hearing_date"),
                                # "role": get_dict_key(thedict=row, key="role"),
                                # "cause_action": get_dict_key(thedict=row, key="cause_action"),
                                # "content": get_dict_key(thedict=row, key="content"),
                                "brief": get_dict_key(thedict=row, key="case_no"),

                            }
                        )
                        satrt += 1
                elif classify == "失信信息":
                    re_date = (today + offset).strftime('%Y-%m-%d')
                    sql = "SELECT * FROM  {} WHERE name='{}' and date>='{}' order by date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and date>='{}' order by date ;".format(
                        tb, name,
                        re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                # "final_duty": get_dict_key(thedict=row, key="final_duty"),
                                "time": get_dict_key(thedict=row, key="date"),
                                # "role": get_dict_key(thedict=row, key="role"),
                                # "execution_status": get_dict_key(thedict=row, key="execution_status"),
                                "title": get_dict_key(thedict=row, key="execution_desc"),
                                "brief": get_dict_key(thedict=row, key="execution_status"),

                            }
                        )
                        satrt += 1
                elif classify == "被执行":
                    re_date = (today + offset).strftime('%Y/%m/%d')
                    sql = "SELECT * FROM  {} WHERE name='{}' and case_date>='{}' order by case_date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and case_date>='{}' order by case_date ;".format(
                        tb, name,
                        re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                "title": get_dict_key(thedict=row, key="case_number"),
                                "time": get_dict_key(thedict=row, key="case_date"),
                                "brief": get_dict_key(thedict=row, key="amount"),
                                # "role": get_dict_key(thedict=row, key="role"),
                                # "court": get_dict_key(thedict=row, key="court"),
                                # "execution_desc": get_dict_key(thedict=row, key="execution_desc"),

                            }
                        )
                        satrt += 1
                elif classify == "裁判文书":
                    re_date = (today + offset).strftime('%Y/%m/%d')
                    sql = "SELECT * FROM  {} WHERE name='{}' and date>='{}' order by date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)
                    # print(1111, sql)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and date>='{}' order by date ;".format(
                        tb, name,
                        re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                "time": get_dict_key(thedict=row, key="date"),
                                "title": get_dict_key(thedict=row, key="title"),
                                "brief": get_dict_key(thedict=row, key="judgeresult"),
                                # "role": get_dict_key(thedict=row, key="role"),
                                # "type": get_dict_key(thedict=row, key="type"),
                                # "case_cause": get_dict_key(thedict=row, key="case_cause"),
                                # "doc_type": get_dict_key(thedict=row, key="doc_type"),

                            }
                        )
                        satrt += 1
                elif classify == "司法冻结":
                    re_date = (today + offset).strftime('%Y/%m/%d')
                    sql = "SELECT * FROM  {} WHERE name='{}' and detail_public_date>='{}' order by detail_public_date LIMIT {} OFFSET {};".format(
                        tb, name, re_date, page_len, (page - 1) * page_len)

                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    sql3 = "SELECT count(*) FROM  {} WHERE name='{}'  and detail_public_date>='{}' order by detail_public_date ;".format(
                        tb, name,
                        re_date)

                    cursor.execute(sql3)
                    rows3 = cursor.fetchall()
                    total_num = rows3[0].get("count(*)")
                    total_page = int(total_num / page_len)
                    if total_num % page_len != 0:
                        total_page += 1

                    # satrt = 1 + page_len * (page - 1)
                    thelist = list()
                    for row in rows:
                        thelist.append(
                            {
                                "code": satrt,
                                "time": get_dict_key(thedict=row, key="detail_public_date"),
                                # "status": get_dict_key(thedict=row, key="status"),
                                "title": get_dict_key(thedict=row, key="detail_assist_item"),
                                "brief": get_dict_key(thedict=row, key="number"),
                                # "type": get_dict_key(thedict=row, key="type"),
                                # "case_cause": get_dict_key(thedict=row, key="case_cause"),
                                # "doc_type": get_dict_key(thedict=row, key="doc_type"),

                            }
                        )
                        satrt += 1
                else:
                    thelist = list()
                    total_num = 0

                static["infolist"] = thelist
                static["number"] = total_num

                """
                "裁判文书": "screen5_judge_doc",
                "司法冻结": "screen5_judicial_freezing",

                "行政处罚": "screen5_adm_penalty",
                "法院公告": "screen5_court_notice",
                "开庭公告": "screen5_court_session_notice",
                "失信信息": "screen5_default",
                "被执行": "screen5_ent_by_execution",

                """

        else:
            total_num = 0
            total_page = 0
        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page, "data": static}
        return result


# 5.4
class SelfSentimentView(BaseView):

    def get(self, request):
        data = request.GET.copy()

        page = int(data.get("page", 1))
        page_len = int(data.get("page_len", 10))
        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        classify = data.get("classify", "正向")
        if classify == "正向":
            tb = "screen5_ent_pos_senti"
        else:
            tb = "screen5_ent_neg_senti"

        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=-6 * 30)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y/%m/%d')

        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT * FROM  {} WHERE name='{}' and time >='{}' order by time desc LIMIT {} OFFSET {};".format(tb,
                                                                                                                    name,
                                                                                                                    re_date,
                                                                                                                    page_len,
                                                                                                                    (
                                                                                                                                page - 1) * page_len)
            cursor.execute(sql)
            rows = cursor.fetchall()

            sql3 = "SELECT count(*) FROM  {} WHERE name='{}' and time >='{}' order by time desc;".format(tb, name,
                                                                                                         re_date)

            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            total_num = rows3[0].get("count(*)")
            total_page = int(total_num / page_len)
            if total_num % page_len != 0:
                total_page += 1

        sentiment = list()
        satrt = 1 + page_len * (page - 1)
        for row in rows:
            # d = get_dict_key(thedict=row, key="brief")
            # if d == "NaN" or d == "(空白)":
            d = get_dict_key(thedict=row, key="title")

            sentiment.append(
                {
                    "code": satrt,
                    "title": d,
                    "url": get_dict_key(thedict=row, key="url"),
                    "dateTime": get_dict_key(thedict=row, key="time"),
                    "brief": get_dict_key(thedict=row, key="brief"),

                })
            satrt += 1

        res = {

            "name": name,
            "classify": classify,
            "sentiment": sentiment,
        }

        result = {"page": page, "page_len": page_len, "total_num": total_num, "total_page": total_page,
                  "data": res}
        return result