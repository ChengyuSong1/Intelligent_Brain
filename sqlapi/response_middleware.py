# coding=utf-8
import json

from django.db import models
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


from utils.responseutil import baseRespData, CJsonEncoder


class UserLoginMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if isinstance(response, dict):
            common_dict = {'code': 200, 'msg': "success", 'data': response}
            response = HttpResponse(json.dumps(common_dict, cls=CJsonEncoder, ensure_ascii=False),
                                    content_type="application/json;charset=utf-8")
        elif isinstance(response, list):
            common_dict = {'code': 200, 'msg': "success", 'data': response}
            response = HttpResponse(json.dumps(common_dict, cls=CJsonEncoder, ensure_ascii=False),
                                    content_type="application/json;charset=utf-8")
        elif isinstance(response, models.Model):
            common_dict = {'code': 200, 'msg': "success", 'data': response}
            response = HttpResponse(json.dumps(common_dict, cls=CJsonEncoder, ensure_ascii=False),
                                    content_type="application/json;charset=utf-8")
        elif isinstance(response, str):
            data = {'code': 501, 'msg': response, 'data': {}}
            response = HttpResponse(json.dumps(data, cls=CJsonEncoder, ensure_ascii=False),
                                    content_type="application/json;charset=utf-8")
        elif isinstance(response, tuple):
            data = {'code': response[0], 'msg': response[1], 'data': {}}
            response = HttpResponse(json.dumps(data, cls=CJsonEncoder, ensure_ascii=False),
                                    content_type="application/json;charset=utf-8")
        return response
