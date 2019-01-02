# coding=utf-8
# author=whitefirer

from server import log
from server.status import make_result, APIStatus, HTTPStatus
from server.meta.decorators import make_decorator, Response

from flask_restful import abort

import re
import decimal


class Hb(object):
    @staticmethod
    @make_decorator
    def check_payload(payload, **kwargs):
        try:
            if None == payload.get('hb_id') \
                or None == payload.get('node_id') \
                or None == payload.get('click_time'):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='缺少参数'))

            return Response(payload=payload, **kwargs)

        except Exception as e:
            log.warn('检查红包参数有误: [error: %s] [payload: %s]' % (str(e), payload), exc_info=True)
            raise e

