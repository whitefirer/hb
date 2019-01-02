# coding=utf-8
# author=qiao
from flask import make_response, jsonify

from server.status import APIStatus, to_http_status

Ok = {"msg": "成功", "status": APIStatus.Ok}
NoUser = {"msg": "无此用户", "status": APIStatus.DataAddError}
ExistsUser = {"msg": "用户已存在", "status": APIStatus.DataAddError}
DataEditError = {"msg": "操作失败", "status": APIStatus.DataEditError}
FileError = {"msg": "文件错误", "status": APIStatus.DataEditError}
TimeError = {"msg": "时间错误", "status": APIStatus.DataEditError}

DownDataBusy = {"msg": "上个下载未运行完成", "status": APIStatus.DataEditError}
Empty = {"msg": "成功", "data": {}, "status": APIStatus.Ok}
EmptyList = {"msg": "成功", "data": {"list": [], "total": 0}, "status": APIStatus.Ok}
EmptyOldList = {"msg": "成功", "data": [], "total": 0, "status": APIStatus.Ok}


class MessageException(Exception):
    def __init__(self, message):
        self.message = message


def message_handler(e):
    if isinstance(e, MessageException):
        return make_response(jsonify(e.message), to_http_status(e.message['status']))
    raise e


class Error(MessageException):
    def __init__(self, msg):
        self.message = {"msg": msg, "status": APIStatus.BadRequest}
