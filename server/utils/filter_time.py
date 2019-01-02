# coding=utf-8
# author=qiao
import time
import datetime


class FilterTime(object):

    @staticmethod
    def datetime_to_int(t: datetime.date):
        assert isinstance(t, datetime.date)
        return int(time.mktime(t.timetuple()))

    @staticmethod
    def int_to_str(t: int, format_str='%Y-%m-%d %H:%M:%S'):
        if not str(t).isdigit():
            return t
        if int(t) == 0:
            return '无'
        return time.strftime(format_str, time.localtime(int(t)))

    @staticmethod
    def str_to_int(t: str, format_str='%Y-%m-%d %H:%M:%S'):
        if not isinstance(t, str):
            return t
        return int(time.mktime(time.strptime(t, format_str)))

    @staticmethod
    def tuple_to_start_int(*args: list) -> int:
        # 输入一个时间元组, 获取 这个时间开头的秒数
        if not(len(args) == 3 and all([str(x).isdigit() for x in args])):
            raise ValueError('')
        return FilterTime.str_to_int("{0}-{1}-{2} 00:00:00".format(*args))

    @staticmethod
    def tuple_to_end_int(*args: list) -> int:
        # 输入一个时间元组, 获取 这个时间结束的秒数
        if not(len(args) == 3 and all([str(x).isdigit() for x in args])):
            raise ValueError('')

        return FilterTime.str_to_int("{0}-{1}-{2} 23:59:59".format(*args))

    @staticmethod
    def get_month_start_end(t: datetime.date):
        # 给一个时间 获取, 该时间的月份的 起始范围
        first = time.mktime(t.timetuple())
        if t.month == 12:
            # 跨年
            last = time.mktime(datetime.date(t.year + 1, 1, 1).timetuple()) - 1
        else:
            last = time.mktime(datetime.date(t.year, t.month + 1, 1).timetuple()) - 1
        return int(first), int(last)

    @staticmethod
    def range_days(start: tuple, end: tuple):
        for x in [start, end]:
            if not (len(x) == 3 and all([str(y).isdigit() for y in x])):
                raise ValueError('')
        start = datetime.date(*start)
        end = datetime.date(*end)
        while end > start:
            yield start
            start += datetime.timedelta(days=1)

    @staticmethod
    def range_months(start: tuple, end: tuple) -> [datetime.date, datetime.date]:
        for x in [start, end]:
            if not (len(x) in (2, 3) and all([str(y).isdigit() for y in x])):
                raise ValueError('')
        _start = datetime.date(start[0], start[1], 1)
        end = datetime.date(end[0], end[1], 1)
        while end > _start:
            yield _start
            if _start.month == 12:
                _start = datetime.date(_start.year + 1, 1, 1)
            else:
                _start = datetime.date(_start.year, _start.month + 1, 1)

    @staticmethod
    def readable_time(t: int):
        if t < 60:
            return '1分钟'
        elif t < 60*60:
            return '%s分钟' % int(t/60)
        elif t < 60*60*24:
            return '%s小时' % int(t/(60*60))
        else:
            return '%s天' % int(t/(60*60*24))
