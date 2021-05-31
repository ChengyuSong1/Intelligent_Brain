import json
import time
import copy
import logging
import traceback

from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BaseView(View):
    page_count = 10

    def get(self, *args, **kwargs):
        return HttpResponse(status=405)

    def post(self, *args, **kwargs):
        return HttpResponse(status=405)

    def put(self, *args, **kwargs):
        return HttpResponse(status=405)

    def delete(self, *args, **kwargs):
        return HttpResponse(status=405)

    def options(self, *args, **kwargs):
        data = {'code': 200, 'msg': "success", 'data': {}}
        return HttpResponse('{}'.format(data))

    def get_body_data(self, request):
        try:
            body = copy.deepcopy(request.body)
            data = json.loads(body.decode().replace(chr(0xa0), ''))
            data["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        except Exception as e:
            data = request.body.decode('utf-8')
        return data

    def pager(self, object_list, pagenum):
        """分页工具
        object_list：数据库结果
        pagenum：第几页
        page_count：每页条数"""
        page_count = self.page_count
        paginator = Paginator(object_list, page_count)
        try:
            res = paginator.page(pagenum)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)
        return paginator, res

    def get_page_data(self, model_obj, page):
        total_num = model_obj.count()
        result = list()
        if page is not None:
            paginator, res = self.pager(model_obj, page)
            result = res.object_list
        pagename = int(total_num / self.page_count)
        if (total_num % self.page_count) != 0:
            pagename += 1
        res = {
            "data_list": result,
            "total_num": total_num,
            "total_page": pagename,
            "page": page,
        }
        return res

    def get_key_num(self, all_data, key, color):
        c3num0 = [i.get(key) for i in list(all_data.values()) if i.get(key) == color]
        return len(c3num0)

    def get_key_num_big(self, all_data, key, color):
        c3num0 = [i.get(key) for i in list(all_data.values()) if (i.get(key) > color) and (int(i.get(key))) != 9999999999]
        return len(c3num0)

    def get_key_num_small(self, all_data, key, color):
        c3num0 = [i.get(key) for i in list(all_data.values()) if (i.get(key) < color) and (int(i.get(key))) != 9999999999]
        return len(c3num0)
