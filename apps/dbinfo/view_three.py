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


# 3.1
class TaxationStaticView(BaseView):

    def get(self, request):
        data = request.GET.copy()
        page = int(data.get("page", 1))

        color_dict = {"红": "c1", "黄": "c2", "绿": "c3"}

        name = data.get("name", "")
        year = data.get("year", time.strftime('%Y', time.localtime(time.time())))
        year = int(year)

        year1 = year
        year_data = dict()
        month_data = dict()
        all_month_data = dict()
        all_year_data = dict()
        laset_year_all_month_data = dict()
        shuifudict = dict()
        shuiallyear = dict()
        jingying_dict = dict()
        with MysqlDB(database=RPDSQL) as cursor:
            sql = "SELECT *,sum(city_maintenance_and_construction_tax+additional_education_tax+local_additional_education_tax) as vat_additional_tax FROM  screen3_year where enterprise_name='{}' group by year order by year desc;".format(name)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                year_data = rows[0]

            for row in rows:
                all_year_data[row["year"]] = row
            year1 = year

            sql2 = "SELECT * FROM  screen3_tax_revenue where ent_name='{}' and year={} order by month desc;".format(name, year1)
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            for row in rows2:
                all_month_data[row["month"]] = row

            if len(rows2) > 0:
                month_data = rows2[0]

            sql3 = "SELECT * FROM  screen3_tax_revenue where ent_name='{}' and year={} order by month desc;".format(
                name, year1-1)
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            for row in rows3:
                laset_year_all_month_data[row["month"]] = row

            sql4 = "SELECT * FROM  screen3_tax_revenue_ratio where ent_name='{}' order by year desc;".format(name)
            cursor.execute(sql4)
            rows4 = cursor.fetchall()
            if len(rows2) > 0:
                shuifudict = rows4[0]

            for row in rows4:
                shuiallyear[row["year"]] = row

            sql5 = "SELECT * FROM  screen3_tax_revenue where ent_name='{}' and year={} order by month desc;".format(name, year)
            # print(sql5)
            cursor.execute(sql5)
            rows5 = cursor.fetchall()
            if len(rows5) > 0:
                jingying_dict = rows5[0]

        # year_data = all_year_data.get(year, {})

        for k in [year_data, month_data]:
            for k1 in list(k.keys()):
                v1 = str(k.get(k1))
                if v1 in ["*", "-1"]:
                    del k[k1]

        five_years = get_five_year()
        months = [i for i in range(1, 13)]
        # last_year = year1 - 1
        last_year = year1

        peopleNum = [get_dict_key(thedict=all_year_data.get(i, {}), key="employee") for i in [i for i in range(last_year-5, last_year+1)]]
        # 税负企业
        qy_num1 = [get_dict_key(thedict=shuiallyear.get(i, {}), key="tax_revenue_ratio", units=0.01) for i in [i for i in range(last_year-4, last_year+1)]]
        # 税负行业
        hy_num1 = [get_dict_key(thedict=shuiallyear.get(i, {}), key="industry_tax_revenue_ratio_rate", units=0.01) for i in [i for i in range(last_year-4, last_year+1)]]
        # // 区级税收收入占全区比例的波动比例
        barChart = [get_dict_key(thedict=all_month_data.get(i, {}), key="dstr_tax_incm_fluctuation_rate_compare") for i in months]
        barChart_year = year1
        clol = [get_dict_key(thedict=all_month_data.get(i, {}), key="dstr_tax_incm_fluctuation_rate_compare_rate") for i in months]
        collist = [color_dict.get(i, get_random_color()) for i in clol]

        lineChart = [get_dict_key(thedict=laset_year_all_month_data.get(i, {}), key="dstr_tax_incm_fluctuation_rate_compare") for i in months]
        lineChart_year = year1-1
        #
        qy_growth = [get_dict_key(thedict=all_month_data.get(i, {}), key="ent_tax_incm_fluctuation_rate_with_ctry_rate") for i in months]
        hy_growth = [get_dict_key(thedict=all_month_data.get(i, {}), key="industry_tax_incm_fluctuation_rate_with_ctry_rate") for i in months]

        # 营业收入1_to_X_month_accum_rev_incm
        yin_gye_shou_ru, ying_ye_unit = get_unit_num(thedict=jingying_dict, key="1_to_X_month_accum_rev_incm", unit="元")
        # 企业利润1_to_X_month_accum_profit
        qi_ye_li_run, qi_ye_li_run_unit = get_unit_num(thedict=jingying_dict, key="1_to_X_month_accum_profit", unit="元")
        # 总税收入accum_ent_total_tax_incm
        zssr, zssr_unit = get_unit_num(thedict=jingying_dict, key="accum_ent_total_tax_incm", unit="元")
        # 地方级税收avg_area_accum_tax_incm_contr
        dfjss, dfjss_unit = get_unit_num(thedict=jingying_dict, key="local_accum_tax_incm", unit="元")
        # 区级税收dstr_accum_ent_tax_incm
        qjss, qjss_unit = get_unit_num(thedict=jingying_dict, key="dstr_accum_ent_tax_incm", unit="元")

        #
        v1, n1 = get_unit_num(thedict=year_data, key="value_added_tax")
        v2, n2 = get_unit_num(thedict=year_data, key="enterprise_income_tax")
        v3, n3 = get_unit_num(thedict=year_data, key="individual_income_tax")
        v4, n4 = get_unit_num(thedict=year_data, key="stamp_tax")
        v5, n5 = get_unit_num(thedict=year_data, key="city_maintenance_and_construction_tax")
        v6, n6 = get_unit_num(thedict=year_data, key="Increment_tax_on_land_value")
        v7, n7 = get_unit_num(thedict=year_data, key="additional_education_tax")
        v8, n8 = get_unit_num(thedict=year_data, key="local_additional_education_tax")
        v9, n9 = get_unit_num(thedict=year_data, key="vat_additional_tax")

        fenshuisort = [['增值税', v1, n1, 'true', get_dict_key(thedict=year_data, key="ent_add_on_tax_dstr_ratio")],
                       ['企业所得税', v2, n2, 'true', get_dict_key(thedict=year_data, key="ent_value_added_tax_dstr_ratio")],
                       ['个人所得税', v3, n3, 'true', get_dict_key(thedict=year_data, key="ent_individual_tax_dstr_ratio")],
                       ['印花税', v4, n4, 'false', get_dict_key(thedict=year_data, key="")],
                       ['土地增值税', v6, n6, 'true', get_dict_key(thedict=year_data, key="ent_land_tax_added_dstr_ratio")],
                       ['增值税附加税', v9, n9, 'false', get_dict_key(thedict=year_data, key="")]
                       ]
        # 降序
        fenshuisort.sort(key=lambda x:x[1], reverse=True)

        static = {
            "name": name,
            "year": year,
            # 模块1：企业经营状况分析
            "speech": "累计税收分析",
            "operate": {
                # 月度营收
                "title": "1至{}月企业经营情况分析".format("2"),
                "monthRevenue": {
                    "number": get_dict_key(thedict=month_data, key="monthly_income", units=10000),
                    "unit": "万",
                    "tb": get_dict_key(thedict=month_data, key="monthly_income_change_by_year"),   # 同比
                    "hytb": get_dict_key(thedict=month_data, key="industry_monthly_income_incremental_rate"),   # 增速同行业比
                    "zb": get_dict_key(thedict=month_data, key="monthly_income_by_region_rate_change"),     # 全区占比
                },
                # 1月至x月企业累计营业收入
                "lj_income": {
                    "number": yin_gye_shou_ru,
                    "tb": get_dict_key(thedict=jingying_dict, key="1_to_X_month_accum_rev_incm_ratio"),   # 同比
                    "speech": "累计营业收入",
                    "unit": ying_ye_unit,
                    "color": get_dict_key(thedict=jingying_dict, key="industry_1_to_X_month_accum_rev_incm_ratio_color"),
                    "thy_zs_b": get_dict_key(thedict=jingying_dict, key="industry_1_to_X_month_accum_rev_incm_ratio"),

                },
                # 1月至x月企业利润
                "lr_income": {
                    "number": qi_ye_li_run,
                    "tb": get_dict_key(thedict=jingying_dict, key="1_to_X_month_accum_profit_ratio"),  # 同比
                    "hy_tb": get_dict_key(thedict=jingying_dict, key="industry_1_to_X_month_accum_profit_ratio"),  # 同行业增速比
                    "speech": "企业利润",
                    "unit": qi_ye_li_run_unit,
                    "ly_lv": get_dict_key(thedict=jingying_dict, key="profit_rate"),  # 利润率
                    "ly_lv_tb": get_dict_key(thedict=jingying_dict, key="profit_rate_ratio"),  # 利润率同比

                },
                # 营收变化情况
                "ys_change": {

                    "dj_tb": get_dict_key(thedict=jingying_dict, key="revenue_by_area"),  # 地均
                    "rj_tb": get_dict_key(thedict=jingying_dict, key="revenue_by_emp"),  # 人均
                    "rj_thy": get_dict_key(thedict=jingying_dict, key="industry_revenue_by_emp"),  # 人均同行业
                    "quanqu_zb": get_dict_key(thedict=jingying_dict, key="revenue_by_dstr"),  # 全区

                    "dj_color": get_dict_key(thedict=jingying_dict, key="revenue_by_area_color"),       # 地均
                    "rj_tb_color": get_dict_key(thedict=jingying_dict, key="revenue_by_emp_color"),    # 人均
                    "rj_thy_color":  get_dict_key(thedict=jingying_dict, key="industry_revenue_by_emp_color"),  # 人均同行业
                    "quanqu_zb_color": get_dict_key(thedict=jingying_dict, key=""),  # 全区
                },

                # 本地缴纳社保员工比例同比变化
                "trend": {
                    "year": [i for i in range(last_year-5, last_year+1)],
                    # 五年人数
                    "peopleNum": {
                        "num": peopleNum,
                        # "unit": "%"
                    },
                    # 变化率
                    "incomeTax": get_dict_key(thedict=year_data, key="employee_change_rate"),
                    "year_num": get_dict_key(thedict=year_data, key="year"),

                },

            },
            # 人地均税收监测
            "shuishou_jiance": {
                "title": "1至{}月人地均税收监测".format("4"),
                "year": get_dict_key(thedict=month_data, key="year"),
                "rj_fwb_pm": get_dict_key(thedict=month_data, key="dstr_empl_avg_tax_incm_rank"),  # 人均区级收入服务包企业排名
                "rj_sh_gx": get_dict_key(thedict=month_data, key="empl_avg_accum_tax_incm_contr", units=10000),      # 人均税收贡献
                "rj_unit": "万元/人",                       # 人均单位
                "rj_tb": get_dict_key(thedict=month_data, key="empl_avg_accum_tax_incm_contr_compare_last_year_ratio"),                    # 人均同比
                "rj_hy_tb": get_dict_key(thedict=month_data, key="industry_empl_avg_accum_tax_incm_contri_ratio"),                 # 人均同行业比

                "dj_fwb_pm": get_dict_key(thedict=month_data, key="dstr_area_avg_tax_incm_rank"),             # 地均区级收入服务包企业排名
                "dj_sh_gx": get_dict_key(thedict=month_data, key="avg_area_accum_tax_incm_contr", units=10000),  # 地均税收贡献
                "dj_unit": "万元/㎡",                    # 地均单位
                "dj_tb": get_dict_key(thedict=month_data, key="area_avg_accum_tax_incm_contr_compare_last_year_ratio"),                 # 地均同比
                "dj_hy_tb": get_dict_key(thedict=month_data, key=""),              # 地均同行业比
            },
            #  //模块2：企业税负监测
            "fu_wu_bao_qy_num": get_dict_key(thedict=shuifudict, key="serv_pack_indus_ent_num"),
            "taxRate": get_dict_key(thedict=shuifudict, key="tax_revenue_ratio", units=0.01),  # 税负率
            "taxRate_tb": get_dict_key(thedict=shuifudict, key="tax_revenue_ratio_change_by_year"),  # 税负率
            "taxRate_tb_color": get_dict_key(thedict=shuifudict, key="tax_revenue_ratio_color"),  # 税负率
            "taxRateRank": get_dict_key(thedict=shuifudict, key="tax_revenue_ratio_rank"),  # 税负率同行业排名
            "taxRateRank_th": get_dict_key(thedict=shuifudict, key="industry_tax_revenue_ratio"),  # 税负率同行业排名
            "taxRateRank_th_color": get_dict_key(thedict=shuifudict, key="industry_tax_revenue_ratio_color"),  # 税负率同行业排名
            "quan_qu_tonghang_taxRate": get_dict_key(thedict=shuifudict, key="industry_tax_revenue_ratio_rate", units=0.01),  # 全区同行业税负率
            # 税负率五年变化值及趋势
            "lineChart": {
                "year": [i for i in range(last_year-4, last_year+1)],
                # 企业 没字段
                "qy_num": qy_num1,
                # 行业
                "hy_num": hy_num1,
                "unit": "%",

            },

            #   //模块5：企业税收数据
            "taxData": {
                # //总收入
                "year": get_dict_key(thedict=month_data, key="year"),
                "title": "1至{}月企业税收数据分析".format("4"),
                "taxCount": {
                    "number": zssr,
                    "unit": zssr_unit,
                    "tb": get_dict_key(thedict=month_data, key="1_to_X_month_total_tax_incm_ratio_change"),
                },
                # //区收入
                "q_taxCount": {
                    "number":  qjss,
                    "unit": qjss_unit,
                    "tb": get_dict_key(thedict=month_data, key="1_to_X_month_local_tax_incm_ratio_change"),
                },
                # //地收入
                "d_taxCount": {
                    "number":  dfjss,
                    "unit": dfjss_unit,
                    "tb": get_dict_key(thedict=month_data, key="ratio_change_by_area"),
                },
                #  //区税收排名
                "q_taxCountRank": get_dict_key(thedict=month_data, key="dstr_tax_incm_compare_dstr_rank"),
                # 税收拉动率
                "pullRate": get_dict_key(thedict=month_data, key="dstr_tax_incm_contr_rate"),
                "speech": "1至{}月区级税收拉动率".format("4"),

                # //区级税收收入占全区比例的波动比例
                "q_taxShare": {
                    "year": months,
                    "last_year": last_year,
                    "barChart": barChart,
                    "barChart_year": barChart_year,
                    "lineChart": lineChart,
                    "lineChart_year": lineChart_year,
                    "color": collist,
                    "unit": "%",

                },
                # //月度区级税收收入波动比例
                "month_taxShare": {
                    "year": months,
                    # 企业
                    "qy_growth": qy_growth,
                    # 行业
                    "hy_growth": hy_growth,
                    "unit": "%"
                },
                # //N种税,年度的增值税--->城镇土地使用税
                # 第42行企业分税种信息展示，仅展示
                # “增值税”、1
                # “企业所得税”、2
                # “城市市维护建设税”、
                # “印花税”、
                # “个人所得税”、
                # “土地增值税”、
                # “教育费附加收入”
                # “地方教育附加收入”
                "tax_FanChart": {
                    "name": [
                        # "增值税",  # true 1
                        # "企业所得税",  # true2
                        # "个人所得税",  # true4
                        # "印花税",  # 5
                        # # "城市维护建设税",  ####8
                        # "土地增值税",  # true15
                        # # "教育费附加收入",
                        # # "地方教育附加收入",
                        # "增值税附加税",
                        fenshuisort[0][0],
                        fenshuisort[1][0],
                        fenshuisort[2][0],
                        fenshuisort[3][0],
                        fenshuisort[4][0],
                        fenshuisort[5][0],
                    ],
                    "number": [
                        # v1,
                        # v2,
                        # v3,
                        # v4,
                        # # v5,
                        # v6,
                        # # v7,
                        # # v8,
                        # v9,
                        fenshuisort[0][1],
                        fenshuisort[1][1],
                        fenshuisort[2][1],
                        fenshuisort[3][1],
                        fenshuisort[4][1],
                        fenshuisort[5][1],
                    ],
                    "unit": [
                        # n1,  # 1
                        # n2,
                        # n3,
                        # n4,  # 5
                        # # n5,
                        # n6,
                        # # n7,
                        # # n8,
                        # n9,
                        fenshuisort[0][2],
                        fenshuisort[1][2],
                        fenshuisort[2][2],
                        fenshuisort[3][2],
                        fenshuisort[4][2],
                        fenshuisort[5][2],
                    ],

                    "is_ld": [
                        # "true",
                        # "true",
                        # "true",
                        # "flase",
                        # # "flase",
                        # "true",
                        # # "flase",
                        # # "flase",
                        # "flase",
                        fenshuisort[0][3],
                        fenshuisort[1][3],
                        fenshuisort[2][3],
                        fenshuisort[3][3],
                        fenshuisort[4][3],
                        fenshuisort[5][3],

                    ],
                    "ld_num": [
                        # get_dict_key(thedict=year_data, key="ent_add_on_tax_dstr_ratio"),
                        # get_dict_key(thedict=year_data, key="ent_value_added_tax_dstr_ratio"),
                        # get_dict_key(thedict=year_data, key="ent_individual_tax_dstr_ratio"),
                        # get_dict_key(thedict=year_data, key=""),
                        # # get_dict_key(thedict=year_data, key=""),
                        # get_dict_key(thedict=year_data, key="ent_land_tax_added_dstr_ratio"),
                        # # get_dict_key(thedict=year_data, key=""),
                        # # get_dict_key(thedict=year_data, key=""),
                        # get_dict_key(thedict=year_data, key=""),
                        fenshuisort[0][4],
                        fenshuisort[1][4],
                        fenshuisort[2][4],
                        fenshuisort[3][4],
                        fenshuisort[4][4],
                        fenshuisort[5][4],
                    ],
                }
            },

            # # 企业同比数据
            # "ent_tb_data": {
            #     "ent_add_on_tax_dstr_ratio":      get_dict_key(thedict=jingying_dict, key="ent_add_on_tax_dstr_ratio"),
            #     # 企业增值税区级收入同比
            #     "ent_value_added_tax_dstr_ratio": get_dict_key(thedict=jingying_dict, key="ent_value_added_tax_dstr_ratio"),
            #     # 企业企业所得税区级收入同比
            #     "ent_individual_tax_dstr_ratio":  get_dict_key(thedict=jingying_dict, key="ent_individual_tax_dstr_ratio"),
            #     # 企业个人所得税区级收入同比
            #     "ent_land_tax_added_dstr_ratio":  get_dict_key(thedict=jingying_dict, key="ent_land_tax_added_dstr_ratio"),
            #     # 企业土地增值税区级收入同比
            #
            # },
        }
        return static
