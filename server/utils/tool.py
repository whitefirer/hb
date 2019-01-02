# coding=utf-8
# author=whitefirer

class BaseModel(dict):
    """空模板类

    """
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value    

class Model(BaseModel):
    """模型基类"""
    pass