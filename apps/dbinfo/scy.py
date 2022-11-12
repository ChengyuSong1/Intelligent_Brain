from apps.baseview import BaseView
from sqlapi.settings import RPDSQL, JSONDATA_PATH
from utils.database_utils import MysqlDB
from apps.dbinfo.utils import get_dict_key, get_color, get_five_year, get_random_bool, get_one_num, \
    get_random_num, get_ryb, get_random_color, getdate, get_unit_value, get_unit_num



class scy(BaseView):
    def get(self, request):
        data = request.GET.copy()
        result = {}
        all_data = dict()

        with MysqlDB(database=RPDSQL) as cursor:
            #企业数量
            sql = "select count(distinct ent_name) as qysl from qy_ent_tax_data"
            cursor.execute(sql)
            rows = cursor.fetchall()
            qysl = rows[0].get("qysl")
            #地方级收入总量
            sql = "select sum(local_tax_income) as dfjsrzl from qy_ent_tax_data where year ='2021'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            dfjsrzl = rows[0].get("dfjsrzl")
            # 地方级收入占全区地方级收入比例
            sql = " select zz/xx*100 as dfjsrzqqdfjsrbl FROM " \
                  "(select 1 as target,sum(local_tax_income) as zz from qy_ent_tax_data where year='2021') a" \
                  " JOIN " \
                  "(select 1 as target,sum(local_tax_income) as xx from qy_dstr_total_tax_income where year='2021') b " \
                  "on a.target = b.target"
            cursor.execute(sql)
            rows = cursor.fetchall()
            dfjsrzqqdfjsrbl = rows[0].get("dfjsrzqqdfjsrbl")
            #资金支持金额总量
            sql = "select sum(amount) as zjzcjezl from qy_fund_support a, qy_ent_unchange_data b where a.ent_name = b.ent_name and a.year = '2020'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            zjzcjezl = rows[0].get("zjzcjezl")
            # 资金支持金额占全区资金支持金额比例
            sql = "select zz/xx*100 as zjzcjezqqzjzcjebl from"\
                  "(select 1 as target,sum(amount) as zz from qy_fund_support a,qy_ent_unchange_data b where a.ent_name = b.ent_name and a.year = '2020') a"\
                  " join " \
                  "(select 1 as target,sum(amount)as xx from qy_fund_support a where a.year = '2020') b " \
                  "on a.target = b.target"
            cursor.execute(sql)
            rows = cursor.fetchall()
            zjzcjezqqzjzcjebl = rows[0].get("zjzcjezqqzjzcjebl")
            # 营收同比变化
            sql = "select case when ((now_year-last_year)/last_year)*100 >3 then 'c3' when ((now_year-last_year)/last_year)*100 <-3 then 'c1' " \
                  "else 'c2' end as color,count(distinct a.ent_name) from " \
                  "(select ent_name,revenue_income as now_year,(revenue_income)/(revenue_ratio+100) as last_year from qy_ent_revenue_profit_data " \
                  "group by 1,2,3) a " \
                  "group by 1"
            cursor.execute(sql)
            rows = cursor.fetchall()
            ystbbh = rows[0].get("ystbbh")
            # 同行业营收增速比较
            sql = "select case when a.zz-b.zz>3 then 'c3' when a.zz-b.zz<-3 then 'c1' else 'c2' end as color,count(distinct a.ent_name) from " \
                  "(select a.ent_name,b.industry,sum(revenue_income)/sum((revenue_income)/(revenue_ratio+100)) as zz from qy_ent_revenue_profit_data a " \
                  "join qy_ent_tax_data b on a.ent_name=b.ent_name " \
                  "where b.year='2021' and month='4'" \
                  "group by 1,2) a " \
                  "join " \
                  "(select b.industry,sum(revenue_income) /sum((revenue_income)/(revenue_ratio+100)) as zz from qy_ent_revenue_profit_data a " \
                  "join qy_ent_tax_data b on a.ent_name=b.ent_name " \
                  "where b.year='2021' and month='4'" \
                  "group by 1) b" \
                  "on a.industry=b.industry" \
                  "group by 1"
            cursor.execute(sql)
            rows = cursor.fetchall()
            thyyszsbj = rows[0].get("thyyszsbj")
            # 营收总量
            sql = "select sum(revenue_income) as yszl from qy_ent_revenue_profit_data"
            cursor.execute(sql)
            rows = cursor.fetchall()
            yszl = rows[0].get("yszl")
            # 营收同比增速
            sql = "select (sum(b.income)-sum(a.last_year))/sum(a.last_year)*100 as ystbzs from" \
                  "(select ent_name,sum(revenue_income)/sum((revenue_ratio/100)+1) as last_year " \
                  "from qy_ent_revenue_profit_data where revenue_ratio is not null and revenue_ratio <> 0 and revenue_income <> 0 " \
                  "group by 1) a " \
                  "join" \
                  "(select ent_name,sum(revenue_income) as income " \
                  "from qy_ent_revenue_profit_data " \
                  "where revenue_ratio is not null and revenue_ratio <> 0 and revenue_income <> 0 " \
                  "group by 1) b " \
                  "on a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            ystbzs = rows[0].get("ystbzs")
            # 区级收入同比变化
            # sql =
            # cursor.execute(sql)
            # rows = cursor.fetchall()
            # qjsrtbbh = rows[0].get("qjsrtbbh")
            # 与同行业区级收入比较
            # sql = ""
            # cursor.execute(sql)
            # rows = cursor.fetchall()
            # thyqjsrbj = rows[0].get("thyqjsrbj")
            # 区级收入总量
            sql = "select sum(tax_income_by_district) as qjsrzl from qy_ent_tax_data where year = '2021'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            qjsrzl = rows[0].get("qjsrzl")
            # 区级收入同比增速
            sql = "select (sum(b.income)-sum(a.last_year))/sum(a.last_year)*100 as qjsrtbzs from " \
                  "(select ent_name,sum(a.tax_income_by_district) as last_year " \
                  "from qy_ent_tax_data a " \
                  "where a.tax_income_by_district is not null and a.tax_income_by_district <> 0 and a.year = '2020' and a.month in ('1','2','3','4')" \
                  "group by 1) a " \
                  "join" \
                  "(select b.ent_name,sum(b.tax_income_by_district) as income " \
                  "from qy_ent_tax_data b " \
                  "where b.tax_income_by_district is not null and b.tax_income_by_district <> 0 and b.year = '2021' and b.month in ('1','2','3','4')" \
                  "group by 1) b " \
                  "on a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            qjsrtbzs = rows[0].get("qjsrtbzs")
            # 资金支持与区级收入贡献情况
                # 资金支持：
            sql = "select year,sum(amount) as zjzc from qy_fund_support a, qy_ent_unchange_data b where a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            zjzc = rows[0].get("zjzc")
                # 区级收入贡献：
            sql = "select year,sum(tax_income_by_district) as qjsrgx from qy_ent_tax_data group by year"
            cursor.execute(sql)
            rows = cursor.fetchall()
            qjsrgx = rows[0].get("qjsrgx")
            # 利润同比变化
            # sql = ""
            # cursor.execute(sql)
            # rows = cursor.fetchall()
            # lrtbbh = rows[0].get("lrtbbh")
            # 同行业利润增速比较
            # sql = ""
            # cursor.execute(sql)
            # rows = cursor.fetchall()
            # thylrzsbj = rows[0].get("thylrzsbj")
            # 利润总量
            sql = "select sum(profit_income) as lrzl from qy_ent_revenue_profit_data where profit_ratio is not null and profit_ratio <> 0"
            cursor.execute(sql)
            rows = cursor.fetchall()
            lrzl = rows[0].get("lrzl")
            # 利润同比增速
            sql = "select (sum(b.income)-sum(a.last_year))/sum(a.last_year)*100 as lrtbzs from " \
                  "(select ent_name,sum(profit_income)/sum((profit_ratio/100)+1) as last_year " \
                  "from qy_ent_revenue_profit_data " \
                  "where profit_ratio is not null and profit_income is not null and profit_ratio <> 0 and profit_income <> 0 " \
                  "group by 1) a " \
                  "join " \
                  "(select ent_name,sum(profit_income) as income " \
                  "from qy_ent_revenue_profit_data " \
                  "where profit_ratio is not null and profit_income is not null and profit_ratio <> 0 and profit_income <> 0 " \
                  "group by 1) b " \
                  "on a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            lrtbzs = rows[0].get("lrtbzs")
            # 人均区级收入
            sql = "select sum(tax)/sum(employee) as rjqjsr from " \
                  "(select ent_name,sum(tax_income_by_district) as tax " \
                  "from qy_ent_tax_data " \
                  "where year = '2021' and employee <> 0 " \
                  "group by 1) a " \
                  "join" \
                  "(select ent_name,sum(employee) as employee " \
                  "from qy_ent_tax_data " \
                  "where employee <> 0 and month in ('4')" \
                  "group by 1) b " \
                  "on a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            rjqjsr = rows[0].get("rjqjsr")
            # 地均区级收入
            sql = " select sum(tax)/sum(area) as djqjsr from " \
                  "(select ent_name,sum(tax_income_by_district) as tax " \
                  "from qy_ent_tax_data " \
                  "where year = '2021' and area <> 0 " \
                  "group by 1) a " \
                  "join" \
                  "(select ent_name,sum(area) as area " \
                  "from qy_ent_tax_data " \
                  "where area <> 0 and month in ('4')" \
                  "group by 1) b " \
                  "on a.ent_name = b.ent_name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            djqjsr = rows[0].get("djqjsr")
            # 服务包中金融业企业数
            sql = " select count(ent_name) as jryqys from qy_ent_unchange_data where industry = '信息传输、软件和信息技术服务业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            jryqys = rows[0].get("jryqys")
            # 服务包中信息服务企业数
            sql = " select count(ent_name) as xxfwqys from qy_ent_unchange_data where industry = '金融业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            xxfwqys = rows[0].get("xxfwqys")
            # 服务包中房地产业企业数
            sql = " select count(ent_name) as fdcqys from qy_ent_unchange_data where industry = '房地产业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            fdcqys = rows[0].get("fdcqys")
            # 服务包中租赁与商务服务业企业数
            sql = " select count(ent_name) as zlswfwqys from qy_ent_unchange_data where industry = '租赁和商务服务业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            zlswfwqys = rows[0].get("zlswfwqys")
            # 服务包中科学服务业企业数
            sql = " select count(ent_name) as kxfwqys from qy_ent_unchange_data where industry = '科学研究和技术服务业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            kxfwqys = rows[0].get("kxfwqys")
            # 服务包中批发零售业企业数
            sql = " select count(ent_name) as pflsqys from qy_ent_unchange_data where industry = '批发和零售业'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            pflsqys = rows[0].get("pflsqys")

        result = {
            "jbxx": {
                "qysl": qysl,  # 企业数量
                "dfjsrzl": dfjsrzl,  # 地方级收入总量
                "dfjsrzqqdfjsrbl": dfjsrzqqdfjsrbl,  # 地方级收入占全区地方级收入比例
                "zjzcjezl": zjzcjezl,  # 资金支持金额总量
                "zjzcjezqqzjzcjebl": zjzcjezqqzjzcjebl,  # 资金支持金额占全区资金支持金额比例
                "ystbbh": ystbbh,  # 营收同比变化
                "thyyszsbj": thyyszsbj,  # 同行业营收增速比较
                "yszl": yszl,  # 营收总量
                "qjsrtbbh": qjsrtbbh,  # 营收同比增速
                "ystbzs": ystbzs,  # 区级收入同比变化
                "thyqjsrbj": thyqjsrbj,  # 与同行业区级收入比较
                "qjsrzl": qjsrzl,  # 区级收入总量
                "qjsrtbzs": qjsrtbzs,  # 区级收入同比增速
                "zjzc": zjzc,  # 资金支持
                "qjsrgx": qjsrgx,  # 区级收入贡献
                "lrtbbh": lrtbbh,  # 利润同比变化
                "thylrzsbj": thylrzsbj,  # 同行业利润增速比较
                "lrzl": lrzl,  # 利润总量
                "lrtbzs": lrtbzs,  # 利润同比增速
                "rjqjsr": rjqjsr,  # 人均区级收入
                "djqjsr": djqjsr,  # 地均区级收入
                "jryqys": jryqys,  # 服务包中金融业企业数
                "xxfwqys": xxfwqys,  # 服务包中信息服务业企业数
                "fdcqys": fdcqys,  # 服务包中房地产业企业数
                "zlswfwqys": zlswfwqys,  # 服务包中租赁与商务服务业企业数
                "kxfwqys": kxfwqys,  # 服务包中科学服务业企业数
                "pflsqys": pflsqys,  # 服务包中批发零售业企业数
            },
        }
        return result
