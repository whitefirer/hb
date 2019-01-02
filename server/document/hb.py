# coding=utf-8
# author=whitefirer

from server import api
from server.status import APIStatus, AdminAPIStatus
from flask_restplus import fields


NodeModel = api.model('node_model', {
    'hb_id': fields.String(description='红包ID', required=True),
    'data_type': fields.String(description='节点数据类型', required=True),
    'node_data': fields.String(description='节点数据', required=True),
    'click_time': fields.Float(description='点击时间', required=True),
})

response_hb_success = api.response(200, '成功', api.model('response_hb_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.Ok]),
    'data': fields.Nested(model=NodeModel, description='数据')
}))

