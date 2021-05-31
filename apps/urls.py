# coding=utf-8
u"""url映射"""

from django.conf.urls import url

from apps.dbinfo import view_one, view_two, view_three, view_four, view_five, view_one_new


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



]


