# coding=utf-8
# author=whitefirer

from server import api, log
from server.meta.decorators import Response
from server.utils import allow_cross_domain

from flask_restplus.cors import crossdomain
from flask_restplus.resource import Resource

import server.document as document
import server.verifies as verifies
import server.operations as operations
import server.filters as filters

from .request_func import *


@document.response_bad_request
class Email(Resource):
    @staticmethod
    @document.response_forbidden
    @document.response_email_success

    @filters.Email.filter(payload=dict)
    @operations.Email.get_data(payload=dict)
    def get():
        """ 获取邮箱数据 """

        resp = Response(payload={
            
        })

        log.info('邮箱接口请求参数: [payload: %s]' %
                 (resp['payload']))

        return resp

ns = api.namespace('email', description='邮箱接口')
ns.add_resource(Email, '/')