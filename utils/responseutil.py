# coding=utf-8
u"""处理返回的response，处理json"""

# from uno.apps.users.forms import UserForm, LoginForm
from django.template.context_processors import csrf
from django.db import models
import json
from datetime import datetime, date
from decimal import *


def baseRespData(request):
    u"""处理需要返回的数据"""
    common_dict = {}
    common_dict.update(csrf(request))
    common_dict["ip"] = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    # print(common_dict["ip"])
    if request.user.is_authenticated():
        common_dict["is_login"] = True
    if request.session.get('login_times', "no") == "yes":
        common_dict["vcode"] = True
    return common_dict


class CJsonEncoder(json.JSONEncoder):
    u"""格式化json"""

    def default(self, obj):
        u"""重载接口"""
        if isinstance(obj, datetime):
            data = obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            data = obj.strftime('%Y-%m-%d')
        elif isinstance(obj, str):
            try:
                data = date.decode("utf-8")
            except Exception as e:
                data = unicode(obj, errors='ignore')
        elif isinstance(obj, models.Model):
            try:
                data = obj.getDetails()
            except Exception as e:
                data = unicode(str(obj.id), errors='ignore')
        elif isinstance(obj, models.query.QuerySet):
            data = list(obj)
        elif isinstance(obj, Decimal):
            # print("Decimal", Decimal, obj)
            data = float(obj)
        else:
            try:
                data = json.JSONEncoder.default(self, obj)
            except Exception as e:
                # print obj
                print(str(e))
                data = ""
        return data


def periodic_task_json(ptask):
    u"""定时任务转化json"""
    p_list = list()
    for p in ptask:
        p_dict = dict()
        if p is not None:
            if p.id is not None:
                p_dict["id"] = str(p.id)
            if p.name is not None:
                p_dict["name"] = p.name
            else:
                p_dict["name"] = ""
            if p.task is not None:
                p_dict["task"] = p.task
            else:
                p_dict["task"] = ""
            if p.args is not None:
                p_dict["args"] = p.args
            else:
                p_dict["args"] = ""
            if p.kwargs is not None:
                p_dict["kwargs"] = p.kwargs
            else:
                p_dict["kwargs"] = ""
            if p.expires is not None:
                p_dict["expires"] = str(p.expires)
            else:
                p_dict["expires"] = ""
            if p.enabled is not None:
                p_dict["enabled"] = p.enabled
            else:
                p_dict["enabled"] = ""
            if p.exchange is not None:
                p_dict["exchange"] = p.exchange
            else:
                p_dict["exchange"] = ""
            if p.routing_key is not None:
                p_dict["routing_key"] = p.routing_key
            else:
                p_dict["routing_key"] = ""
            if p.queue is not None:
                p_dict["queue"] = p.queue
            else:
                p_dict["queue"] = ""
            if p.last_run_at is not None:
                p_dict["last_run_at"] = str(p.last_run_at)
            else:
                p_dict["last_run_at"] = ""
            if p.total_run_count is not None:
                p_dict["total_run_count"] = p.total_run_count
            else:
                p_dict["total_run_count"] = ""
            if p.date_changed is not None:
                p_dict["date_changed"] = p.date_changed
            else:
                p_dict["date_changed"] = ""
            if p.description is not None:
                p_dict["description"] = p.description
            else:
                p_dict["description"] = ""
            if p.crontab is not None:
                p_dict["crontab"] = str(p.crontab)
            else:
                p_dict["crontab"] = ""
            if p.interval is not None:
                p_dict["interval"] = str(p.interval)
            else:
                p_dict["interval"] = ""
        if p_dict.get("id") is not None:
            p_list.append(p_dict)
    return p_list
