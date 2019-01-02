# coding=utf-8
# author=whitefirer

from flask_restful import abort

from server.status import HTTPStatus, APIStatus, make_result
from server.meta.decorators import make_decorator, Response
from server import log
from server.utils import email

class Email(object):
    @staticmethod
    @make_decorator
    def get_data(payload):
        '''
            获取邮箱数据
        '''

        data = email.get_data(payload)

        return Response(payload=data)
