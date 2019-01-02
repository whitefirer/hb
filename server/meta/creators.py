# coding=utf-8
# author=whitefirer


def StaticClass(name, *args, **kwargs):
    methods = []
    methods.extend(args)
    methods.extend(kwargs.values())

    return type(name, (object,), {
        func.__name__: func for func in methods
    })


class DictModel(dict):
    def __init__(self, *args, **kwargs):
        super(DictModel, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            value = self[key]
            if type(value) == dict:
                value = self[key] = DictModel(value)
                return value
            return value
        except KeyError:
            raise AttributeError(r'"DictModel" object has no attribute "%s"' % key)

    def __setattr__(self, key, value):
        self[key] = value
