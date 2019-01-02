# coding=utf-8
# author=whitefirer

from flask_restful import abort

from server.status import HTTPStatus, APIStatus, make_result
from server.meta.decorators import make_decorator, Response
from server import log
from server.utils import hb

class Hb(object):
    @staticmethod
    @make_decorator
    def get_data(payload):
        '''
            获取红包数据
        '''

        data = hb.get_data(payload)

        return Response(payload=data)
