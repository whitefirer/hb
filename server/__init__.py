# coding=utf-8
# author=whitefirer

from flask import Flask, render_template, Markup, jsonify, session, g, request, redirect
from flask_restplus import Api
from .status import HTTPStatus, make_result, APIStatus
import json
import datetime
import urllib
import logging
import redis
import time

app = Flask(__name__)
app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))
app.jinja_env.filters['mytime'] = lambda v: v % time.time()
app.config.from_object("config.Config") 
app.config['ERROR_404_HELP'] = False
app.secret_key = '2019hongbao'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=6)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
cache = redis.Redis(host='redis', port=6379)

log = logging.getLogger('hb')
level = logging.getLevelName('DEBUG')
log.setLevel(level)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s'))
stream_handler.setLevel(level)
log.addHandler(stream_handler)

api = Api(app, version='4.0.0', title='红包 API 4.0.0',
    description='仅调试模式下开启，<a href="/index/">进入主页</a>', authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Token'
        }
    }, security='apikey', ui=True, doc=app.config['DOC']
)

@app.errorhandler(HTTPStatus.NotFound)
def page_not_found(e):
    return redirect('/index/')


@app.errorhandler(HTTPStatus.InternalServerError)
def internal_server_error(e):
    log.warn('内部服务发生异常: [error: %s]' % (e,), exc_info=True)
    return jsonify(make_result(APIStatus.InternalServerError)), 500


@api.errorhandler(Exception)
def resource_internal_server_error(e):
    log.warn('服务发生异常: [error: %s]' % (e, ), exc_info=True)
    return jsonify(make_result(APIStatus.InternalServerError)), 500


@api.errorhandler(ValueError)
@api.errorhandler(TypeError)
def value_error(e):
    log.warn('服务发生异常: [error: %s]' % (e, ), exc_info=True)
    return jsonify(make_result(APIStatus.InternalServerError)), 500

from .resources import *
from .route import *

