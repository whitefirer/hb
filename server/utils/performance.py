# coding=utf-8
# author=whitefirer

from functools import wraps
import time

def fn_performance(fn):
    def wrapper(function):
        @wraps(function)
        def function_timer(*args, **kwargs):
            t0 = time.time()

            result = function(*args, **kwargs)

            t1 = time.time()

            fn(function, t1-t0)
            return result
        return function_timer
    return wrapper


if __name__ == '__main__':
    @fn_performance(lambda x, y: print(x.__name__, y))
    def for_():
        for i in range(1000000000):
            pass
    for_()