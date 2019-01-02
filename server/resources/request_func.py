# coding=utf-8
# author=whitefirer

from functools import reduce

import html
import tokenize
from flask import session

from flask_restful import abort
from flask_restful import request

from server.status import APIStatus, HTTPStatus, make_result

from server.utils.interval import is_ok_parse, ParseError, Parse
from server.utils.filter_time import FilterTime


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ('xls',)


def get_file(filename):
    file = request.files.get(filename)
    file = file.read().decode("utf-8")
    file = [x.split(',') for x in file.splitlines()]
    return file


def payload_escape(payload):
    """
    " -> &quot;
    """
    for k in payload:
        if isinstance(payload[k], str):
            payload[k] = html.escape(payload[k])
        elif isinstance(payload[k], dict):
            payload[k] = payload_escape(payload[k])
    return payload


def payload_unescape(payload):
    """
    &quot; -> "
    """
    for k in payload:
        if isinstance(payload[k], str):
            payload[k] = html.unescape(payload[k])
        elif isinstance(payload[k], dict):
            payload[k] = payload_unescape(payload[k])
    return payload


def get_token():
    token = request.headers.get('token', None)
    if token:
        return token
    abort(HTTPStatus.UnAuthorized, **make_result(status=APIStatus.UnLogin, msg='用户已下线，请重新登陆'))


def get_session():
    if "login" in session:
        return {"id": session["login"]["id"], "role": session["login"]["role"]}
    abort(HTTPStatus.UnAuthorized, **make_result(status=APIStatus.UnLogin, msg='用户已下线，请重新登陆'))


def get_name_by_session():
    return session["login"]["name"]


def get_user_id_by_session():
    return session["login"]["id"]


def get_user_role_by_session():
    return session["login"]["role"]


def get_payload():
    payload = request.json
    if payload:
        return payload_escape(payload)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='缺少请求数据'))


def get_none_if_empty_payload(key):
    # '' -> None
    if not request.json.get(key, None):
        return None
    return request.json[key]


def get_payload_or_400(key, verbose_name=None):
    value = request.json.get(key, None)
    if value:
        return value
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='payload 缺少请求参数 %s %s' % (verbose_name, key)))

def get_payload_or_emptystring(key, verbose_name=None):
    value = request.json.get(key, None)
    if value:
        return value
    return ''


def get_arg_or_400(key):
    value = request.args.get(key, None)
    if value:
        return value
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='arg 缺少请求参数 %s' % (key, )))


def get_arg_int(key, default=None):
    value = request.args.get(key, default)
    if str(value).lstrip('-').isdigit():
        return int(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_payload_int(key, default=None):
    value = request.json.get(key, default)
    if str(value).lstrip('-').isdigit():
        return int(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_payload_int_or_none(key):
    if key not in request.json.keys():
        return None
    value = request.json.get(key, None)
    if str(value).lstrip('-').isdigit():
        return int(value)
    if not value:
        return None
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_arg_int_or_none(key):
    if key not in request.args.keys():
        return None
    value = request.args.get(key, None)
    if str(value).lstrip('-').isdigit():
        return int(value)
    if not value:
        return None
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_payload_bit_list_int(key, default=None):
    value = request.json.get(key, default)
    if not isinstance(value, list):
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 list' % (key,)))
    if not value:
        return 0
    for i in value:
        if (not str(i).isdigit()) or (int(i) > 2 and i % 2 == 1) or (i == 0):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 中(%s) 错误' % (key, i)))
    return reduce(lambda x, y: x | y, value)


def get_int_time_or_none_payload(key, format_str='%Y-%m-%d %H:%M'):
    # '' -> None
    if not request.json.get(key, None):
        return None
    try:
        return FilterTime.str_to_int(request.json[key], format_str=format_str)
    except ValueError:
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='%s 格式错误' % (key,)))


def get_payload_float(key):
    value = request.json.get(key)
    if str(value).lstrip('-').replace('.', '', 1).isdigit():
        return float(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 float' % (key,)))


def get_payload_float_or_none(key):
    value = request.json.get(key, None)
    if str(value).lstrip('-').replace('.', '', 1).isdigit():
        return float(value)
    if not value:
        return None
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 float' % (key,)))


def get_arg_float_or_none(key):
    value = request.args.get(key, None)
    if str(value).lstrip('-').replace('.', '', 1).isdigit():
        return float(value)
    if not value:
        return None
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 float' % (key,)))


def get_arg(key, default=None):
    return request.args.get(key, default)


def get_none_if_empty_arg(key):
    # '' -> None
    if key not in request.args.keys():
        return None
    return request.args[key] or None


def get_int_time_or_none_arg(key, format_str='%Y-%m-%d'):
    # '' -> None
    if not request.args.get(key, None):
        return None
    try:
        return FilterTime.str_to_int(request.args[key], format_str=format_str)
    except ValueError:
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='%s 格式错误' % (key,)))


def get_all_arg():
    # request.args ImmutableMultiDict 是不可变的
    return request.args.to_dict()


def get_ok_parse(key, verbose_name):
    value = get_payload_or_400(key, verbose_name)
    try:
        is_ok_parse(Parse(value.encode()).parse())
    except (ParseError, tokenize.TokenError):
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='%s 格式错误' % (verbose_name,)))
    return value
