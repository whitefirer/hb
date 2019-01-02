# coding=utf-8
# author=whitefirer


class HTTPStatus:
    # 成功
    Ok = 200

    Success = 302

    # 参数错误
    BadRequest = 400

    # 验证失败
    UnAuthorized = 401

    # 服务器拒绝该请求
    Forbidden = 403

    # 未找到该资源
    NotFound = 404

    # 服务器内部错误
    InternalServerError = 500

    # 服务器超载
    ServiceUnavailable = 503
    

class APIStatus:
    # 成功
    Ok = 100000

    # 请求参数有误
    BadRequest = 100001

    # 服务器内部有误
    InternalServerError = 100002

    # 服务器拒绝此请求
    Forbidden = 100001
    
    # 数据修改\删除\失败
    DataEditError = 200101

    # 数据增加失败
    DataAddError = 200102

    # 没有此用户
    NotUser = 100004

    # 密码错误
    PasswdError = 100005
    
    # 类型错误 
    UserTypeError = 100008

    # 用户未登录
    UnLogin = 100006

    # 验证码错误
    CodeError = 100007

    # 未找到资源
    NotFound = 100404
    
    # 权限拒绝
    Deny = 100500

    # 访问成功
    Success = 100302

    GetUserCouponsError = 100404

    CouponsOwnerError = 100404

    CouponsAmountError = 100404


class AdminAPIStatus(APIStatus):
    Decriptions = {
        APIStatus.Ok: '成功',
        APIStatus.NotFound: '未找到该资源',
        APIStatus.BadRequest: '请求参数有误',
        APIStatus.InternalServerError: '服务器内部错误',
        APIStatus.Forbidden: '权限错误',
        APIStatus.UnLogin: '未登录',
        APIStatus.Success: '成功',
        APIStatus.Deny: '权限不足',
    }


def to_http_status(status):
    return {
        AdminAPIStatus.Ok: HTTPStatus.Ok,
        AdminAPIStatus.BadRequest: HTTPStatus.BadRequest,
        AdminAPIStatus.InternalServerError: HTTPStatus.InternalServerError,
        AdminAPIStatus.Forbidden: HTTPStatus.Forbidden,
        AdminAPIStatus.NotUser: HTTPStatus.Forbidden,
        AdminAPIStatus.PasswdError: HTTPStatus.Forbidden,
        AdminAPIStatus.UnLogin: HTTPStatus.Forbidden,
        AdminAPIStatus.NotFound: HTTPStatus.NotFound,
        AdminAPIStatus.Success: HTTPStatus.Success
    }[status]


def build_result(status, data=None):
    if data is not None:
        return {'status': status, 'msg': AdminAPIStatus.Decriptions[status], 'data': data}
    return {'status': status, 'msg': AdminAPIStatus.Decriptions[status]}


def make_result(status, msg=None, data=None):
    if data is not None:
        return {'status': status, 'msg': msg if msg else AdminAPIStatus.Decriptions[status], 'data': data}
    return {'status': status, 'msg': msg if msg else AdminAPIStatus.Decriptions[status]}


def old_result(status, msg=None, **kwarg):
    temp = {'status': status, 'msg': msg if msg else AdminAPIStatus.Decriptions[status]}
    temp.update(kwarg)
    return temp
