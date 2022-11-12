# coding=utf-8
u"""url映射"""

from django.conf.urls import url

from apps.dbinfo import view_two, view_three, view_four, view_five, view_one_new, scy
from apps.build import build_one, build_two, build_three, build_four, build_five, scenario_1, scenario_2, scenario_3, \
    scy1

urlpatterns = [

]

urlpatterns += [
    # 1.朝阳区重点企业信息
    # url(r"^api/v1/enterprise/info/static$", view_one.InfoStaticView.as_view(), name="info_static"),
    # url(r"^api/v1/enterprise/info/healthy$", view_one.InfoHealthyView.as_view(), name="info_healthy"),
    # url(r"^api/v1/enterprise/info/sentiment$", view_one.InfoSentimentView.as_view(), name="info_sentiment"),

    # 1，static
    url(r"^api/v1/enterprise/info/static_new$", view_one_new.InfoStaticView.as_view(), name="info_static_new"),
    url(r"^api/v1/enterprise/info/healthy_new$", view_one_new.Picshow.as_view(), name="info_healthy_new"),
    url(r"^api/v1/enterprise/info/scy$", scy.scy.as_view(), name="scy"),

    # 1.1 营收
    url(r"^api/v1/enterprise/info/one/static$", view_one_new.InfoStaticOneView.as_view(), name="info_static_one"),
    url(r"^api/v1/enterprise/info/one/healthy$", view_one_new.InfoStaticOneListView.as_view(), name="info_healthy_one"),

    # 1.2 税收
    url(r"^api/v1/enterprise/info/two/static$", view_one_new.InfoStaticTwoView.as_view(), name="info_static_two"),
    url(r"^api/v1/enterprise/info/two/healthy$", view_one_new.InfoStaticOneListView.as_view(), name="info_healthy_two"),

    # 1.3 支持
    url(r"^api/v1/enterprise/info/three/static$", view_one_new.InfoStaticThreeView.as_view(), name="info_static_three"),
    url(r"^api/v1/enterprise/info/three/rank$", view_one_new.InfoRankView.as_view(), name="info_static_three_rank"),

    # 2.企业基本信息
    url(r"^api/v1/enterprise/baseinfo/static$", view_two.BaseinfoStaticView.as_view(), name="baseinfo_static"),           # 朝阳区企业基本信息画像
    url(r"^api/v1/enterprise/baseinfo/sentiment$", view_two.BaseinfoSentimentView.as_view(), name="baseinfo_sentiment"),  # 朝阳区企业基本信息画像

    # 3.企业税收及运营
    url(r"^api/v1/enterprise/taxation/static$", view_three.TaxationStaticView.as_view(), name="taxation_static"),

    # 4,企业政府投入产出页面
    url(r"^api/v1/enterprise/input_output/static$", view_four.InputOutputStaticView.as_view(), name="input_output"),
    url(r"^api/v1/enterprise/visit/info$", view_four.VisitInfoView.as_view(), name="visit_info"),

    # 5，企业变更风险详情
    # 股权
    url(r"^api/v1/enterprise/stock_right/info$", view_five.StockRightView.as_view(), name="stock_right"),
    # 变更信息
    url(r"^api/v1/enterprise/change/info$", view_five.ChangeInfoView.as_view(), name="change_info"),
    # 风险信息
    url(r"^api/v1/enterprise/risk/info$", view_five.RiskInfoView.as_view(), name="risk_info"),
    # 舆情
    url(r"^api/v1/enterprise/self/sentiment$", view_five.SelfSentimentView.as_view(), name="self_sentiment"),









    # 楼宇
    # 屏幕1-朝阳区楼宇总览页面
    # 朝阳区楼宇基本信息和地图
    url(r"^api/v1/build/s1/ly/basicinfomap$", build_one.LyBasicInfoAndMap.as_view(), name="basicInfoMap"),
    # 朝阳区楼宇总体情况
    url(r"^api/v1/build/s1/ly/generalsituation$", build_one.LyGeneralSituation.as_view(), name="generalSituation"),
    # 重点功能区内楼宇情况
    url(r"^api/v1/build/s1/ly/functionarea$", build_one.LyGongNengQu.as_view(), name="gongNengQu"),
    # 各街乡楼宇分析
    url(r"^api/v1/build/s1/ly/gejiexiang$", build_one.LyGeJieXiang.as_view(), name="geJieXiang"),

    # 屏幕2-CBD核心区域楼宇总览页面
    # 模块1 - 总体信息
    url(r"^api/v1/build/s2/cbd/overview$", build_two.CbdOverview.as_view(), name="cbdOverview"),
    # 模块2 - 楼内企业流动情况（1至X月）
    url(r"^api/v1/build/s2/ly/entflow$", build_two.LyEntFlowCondi.as_view(), name="cbdOverview"),
    # 模块3 - 楼宇税收贡献情况
    url(r"^api/v1/build/s2/ly/taxContri$", build_two.LyTaxRevenueContriCondi.as_view(), name="cbdOverview"),

    # 屏幕2.1 157家楼宇内企业流动详情
    # 楼宇空置情况
    url(r"^api/v1/build/s2/ly/qyldxq$", build_three.Lyqyldxq.as_view(), name="lyqyflow"),
    # 楼宇企业流动情况（1至X月）
    url(r"^api/v1/build/s2/ly/qyflow$", build_three.Lyqylr.as_view(), name="lyqyflow"),

    # 屏幕2.2 157家楼宇税收详情
    # 楼宇总税收贡献情况
    url(r"^api/v1/build/s2/ly/lyqycontri$", build_three.Lyqytaxcontri.as_view(), name="lyqycontri"),
    # 楼宇区级收入贡献情况
    url(r"^api/v1/build/s2/ly/lyqjsrcontri$", build_three.Lyqydstrtaxcontri.as_view(), name="lyqycontri"),
    # 楼宇地均、人均收入贡献情况
    url(r"^api/v1/build/s2/ly/lyqyavgcontri$", build_three.Lyqyavgtaxcontri.as_view(), name="lyqycontri"),

    # 屏幕2.3 157家楼宇本异地纳税、楼内行业分布
    # 楼宇内企业行业分布
    url(r"^api/v1/build/s2/ly/lyydnshyfb$", build_three.Lyqyzdhyfb.as_view(), name="lyqycontri"),
    # 楼宇属地纳税与注册情况
    url(r"^api/v1/build/s2/ly/lysdnszcqk$", build_three.lysdnszcqk.as_view(), name="lyqycontri"),


    # 屏幕3-某栋楼宇信息首页
    # 楼内企业基本信息
    url(r"^api/v1/build/s2/ly/lylnbasicinfo$", build_four.lylnbasicinfo.as_view(), name="lyqyinfo"),
    # 楼宇能耗变化情况
    url(r"^api/v1/build/s2/ly/lynhchange$", build_four.lynhchange.as_view(), name="lyqyinfo"),
    # 楼内企业结构
    url(r"^api/v1/build/s2/ly/lyentstruct$", build_four.lyentstruct.as_view(), name="lyqyinfo"),
    # 模块四补充数据-0705
    url(r"^api/v1/build/s2/ly/lyentzb$", build_four.lyentzb.as_view(), name="lyqyinfo"),
    # 楼内企业流动情况分析
    url(r"^api/v1/build/s2/ly/lyentflow$", build_four.lyentflow.as_view(), name="lyqyinfo"),

    # 屏幕4-某栋楼宇经济税收分析
    # 楼宇税收数据（1至X月）
    url(r"^api/v1/build/s2/ly/lytaxdata$", build_five.lytaxdata.as_view(), name="lyqyinfo"),
    # 楼宇属地纳税情况（1至X月）
    # 楼宇税收贡献集中度
    url(r"^api/v1/build/s2/ly/lysdtaxcondi$", build_five.lysdtaxcondi.as_view(), name="lyqyinfo"),
    # 企业税收贡献分类排名（1至X月）
    url(r"^api/v1/build/s2/ly/lyenttaxcontrirank$", build_five.lyenttaxcontrirank.as_view(), name="lyqyinfo"),


    # 场景1
    # 模块一：八个总览数据
    url(r"^api/v1/build/s1/ly/lybasicinfomap$", scenario_1.BasicInfoAndMap.as_view(), name="basicInfoMap"),

    # 模块二：单独楼宇统揽数据
    url(r"^api/v1/build/s1/ly/Lybuilidnginfo$", scenario_1.Lybuilidnginfo.as_view(), name="basicInfoMap"),

    # 模块三：人均区级收入
    url(r"^api/v1/build/s1/ly/lypavg$", scenario_1.lypavg.as_view(), name="basicInfoMap"),

    # 模块四：地均区级收入
    url(r"^api/v1/build/s1/ly/lyareaavg$", scenario_1.lyareaavg.as_view(), name="basicInfoMap"),

    # 模块六：属地纳税情况
    url(r"^api/v1/build/s1/ly/areataxinfo$", scenario_1.areataxinfo.as_view(), name="basicInfoMap"),

    # 模块七：各街乡楼宇分析
    url(r"^api/v1/build/s1/ly/lystreetlyanalysis$", scenario_1.lystreetlyanalysis.as_view(), name="basicInfoMap"),

    # 场景2
    # 模块一：CBD功能区楼宇基本信息和地图
    url(r"^api/v1/build/s1/ly/CBDfunctionareainfo$", scenario_2.CBDfunctionareainfo.as_view(), name="CBDInfo"),

    # 模块二：CBD功能区楼宇税收贡献情况
    url(r"^api/v1/build/s1/ly/CBDfunctionareataxinfo$", scenario_2.CBDfunctionareataxinfo.as_view(), name="CBDInfo"),

    # 模块三：CBD功能区楼宇税收总量
    url(r"^api/v1/build/s1/ly/CBDfunctionlytax$", scenario_2.CBDfunctionlytax.as_view(), name="CBDInfo"),

    # 模块四：CBD功能区楼内企业流动情况
    url(r"^api/v1/build/s1/ly/CBDentflowcondi$", scenario_2.CBDentflowcondi.as_view(), name="CBDInfo"),

    # 模块六：CBD功能区楼宇主导行业分布
    url(r"^api/v1/build/s1/ly/CBDdominantdstr$", scenario_2.CBDdominantdstr.as_view(), name="CBDInfo"),

    # 模块七：CBD功能区楼宇属地纳税情况
    url(r"^api/v1/build/s1/ly/CBDsdtaxinfo$", scenario_2.CBDsdtaxinfo.as_view(), name="CBDInfo"),

    # 模块八：CBD功能区楼宇内企业本地工商注册率
    url(r"^api/v1/build/s1/ly/CBDgsreg$", scenario_2.CBDgsreg.as_view(), name="CBDInfo"),

    # 场景3
    # 模块一：某楼宇基本信息
    url(r"^api/v1/build/s1/ly/lybasicinfo$", scenario_3.lybasicinfo.as_view(), name="entInfo"),

    # 模块二：楼宇税收贡献情况
    url(r"^api/v1/build/s1/ly/lytaxcontricondi$", scenario_3.lytaxcontricondi.as_view(), name="entInfo"),

    # 模块三：楼宇内企业流动情况
    url(r"^api/v1/build/s1/ly/lyentflowcondi$", scenario_3.lyentflowcondi.as_view(), name="entInfo"),

    # 模块四：楼宇能耗排名
    url(r"^api/v1/build/s1/ly/lyenergycost$", scenario_3.lyenergycost.as_view(), name="entInfo"),

    # 模块五：楼内企业结构
    url(r"^api/v1/build/s1/ly/lyentstructure$", scenario_3.lyentstructure.as_view(), name="entInfo"),

    # 模块六：企业属地纳税注册情况
    url(r"^api/v1/build/s1/ly/qysdtaxregcondi$", scenario_3.qysdtaxregcondi.as_view(), name="entInfo"),

    # 模块七：楼内企业类型情况
    url(r"^api/v1/build/s1/ly/lyenttypecondi$", scenario_3.lyenttypecondi.as_view(), name="entInfo"),
    url(r"^api/v1/enterprise/info/scy1$", scy1.scy1.as_view(), name="scy"),
]


