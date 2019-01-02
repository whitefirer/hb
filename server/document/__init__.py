# coding=utf-8
# author=whitefirer


from flask_restplus import fields
from server.status import APIStatus, AdminAPIStatus
from server import api


request_token = api.header('token', type=str, description='登录令牌', required=True)

response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.Ok]),
}))

response_bad_request = api.response(400, '请求参数错误', api.model('response_bad_request', {
    'state': fields.Integer(description=str(APIStatus.BadRequest)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.BadRequest]),
}))

response_unauthorized = api.response(401, '验证失败', api.model('response_unauthorized', {
    'state': fields.Integer(description=str(APIStatus.UnLogin)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.UnLogin]),
}))


response_forbidden = api.response(403, '服务器拒绝该请求', api.model('response_response_forbidden', {
    'state': fields.Integer(description=str(APIStatus.Forbidden)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.Forbidden]),
}))

response_not_found = api.response(404, '未找到资源', api.model('response_not_found', {
    'state': fields.Integer(description=str(APIStatus.NotFound)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.NotFound]),
}))

response_internal_server_error = api.response(500, '内部服务器错误', api.model('response_internal_server_error', {
    'state': fields.Integer(description=str(APIStatus.InternalServerError)),
    'msg': fields.String(description=AdminAPIStatus.Decriptions[APIStatus.InternalServerError]),
}))

from .hb import *
from .email import *
