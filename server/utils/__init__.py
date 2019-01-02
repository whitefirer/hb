# coding=utf-8
# author=whitefirer

from functools import wraps
from flask import make_response, jsonify

import time
import random

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        resp, status = fun(*args, **kwargs)
        rst = make_response(jsonify(resp), status)
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
