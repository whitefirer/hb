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
class Hb(Resource):
    @staticmethod
    @document.response_forbidden
    @document.response_hb_success
    @api.doc(params={'hb_id': '红包ID', 'node_id': '节点ID', 'click_time': '点击时间'})

    @filters.Hb.filter(payload=dict)
    @operations.Hb.get_data(payload=dict)
    @verifies.Hb.check_payload(payload=dict)
    def get():
        """ 获取红包数据 """

        resp = Response(payload={
            "hb_id": get_arg_or_400("hb_id"),
            "node_id":get_arg_or_400("node_id"),
            "click_time": get_arg_float_or_none("click_time"),
        })

        log.info('红包接口请求参数: [payload: %s]' %
                 (resp['payload']))

        return resp

ns = api.namespace('hb', description='红包接口')
ns.add_resource(Hb, '/')