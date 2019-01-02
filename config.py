# coding=utf-8
# author=whitefirer

import os
import datetime 

def get_path(rpath):
    LOCAL_DIR = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(LOCAL_DIR, rpath))

class Config(object):
    DOC = '/doc'#设为空则禁止显示文档
    
    LOG = {
        "level": "DEBUG",
        "fluent": {
            "host": "127.0.0.1",
            "port": 24224,
            "tag": "hb"
        }
    }

    HB201901_CODE = '红包1已领取完'
    HB201902_CODE = '请不要分享给他人，口令：59811381'
