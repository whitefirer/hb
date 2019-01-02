# coding=utf-8
# author=whitefirer

from server import log
from server.status import make_result, APIStatus, HTTPStatus, old_result
from server.meta.decorators import make_decorator
import simplejson as json


class BaseFilter(object):
    @staticmethod
    @make_decorator
    def page(index, count, total, data):
        return old_result(APIStatus.Ok, index=index, count=count, total=total, data=data), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def post(data):
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def put(data):
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def detail(data):
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def delete(data):
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok

from .hb import Hb
from .email import Email