# coding=utf-8
# author=whitefirer

from server import log
from server.status import make_result, APIStatus, HTTPStatus
from server.meta.decorators import make_decorator

import random
import simplejson as json
from . import BaseFilter

class Hb(BaseFilter):
    @staticmethod
    @make_decorator
    def filter(payload):
        return make_result(APIStatus.Ok, data=payload), HTTPStatus.Ok
