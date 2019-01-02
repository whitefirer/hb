# coding=utf-8
# author=whitefirer

import functools
from .errors import *


class Response(dict):
    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)


class DirectResponse(dict):
    def __init__(self, *args, **kwargs):
        super(DirectResponse, self).__init__(*args, **kwargs)


def make_decorator(f):
    @functools.wraps(f)
    def input_params(**params):
        restriction = {}
        values = {}
        for name in params:
            typ = params[name]
            try:
                isinstance(0, typ)
                restriction.update({name: typ})
            except:
                values.update({name: typ})

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_result = func(*args, **kwargs)
                if isinstance(last_result, Response):
                    next_params = {}
                    for k in restriction:
                        value = last_result.get(k, None)
                        if value is None:
                            raise ResponseError("{func_name} missing 1 required positional argument: {key}"
                                                .format(func_name=f.__str__(), key=k))

                        if not isinstance(value, restriction[k]):
                            raise ParameterError('{func_name} {key} must be a {typ}'.format(func_name=f.__str__(),
                                                 key=k, typ=restriction[k].__name__))
                        next_params[k] = value

                    if values:
                        next_params.update(values)
                    return f(**next_params)
                elif isinstance(last_result, DirectResponse):
                    return last_result
                else:
                    raise ResponseError('the {func_name} return value must be a Response or DirectResponse'
                                        .format(func_name=func.__str__()))
            return wrapper
        return decorator

    return input_params


def catch_exception(handler):
    def accept_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return handler(e)
        return wrapper
    return accept_func


if __name__ == '__main__':
    g = {
        'a': 10,
        'b': 20
    }

    def decorator(g, shit, bitch):
        print(g, shit, bitch)
        return Response(a=g['a'], b=g['b'])

    fuck_the_world = make_decorator(decorator)

    @fuck_the_world(g=g, shit=str, bitch=str)
    def flat_func():
        return Response(shit= 'shit', bitch= 'bitch')

    print(flat_func())
