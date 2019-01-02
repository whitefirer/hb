
import tokenize
from io import BytesIO
import math
from decimal import Decimal as D

class ParseError(Exception):
    pass


class Parse(object):
    def __init__(self, text):
        self.tokens = []
        self.index = 0
        for tok in tokenize.tokenize(BytesIO(text).readline):
            if tok.type == tokenize.ENCODING:
                continue
            self.tokens.append(tok)

    def next(self):
        tok = self.tokens[self.index]
        self.index += 1
        return tok

    def peek(self):
        return self.tokens[self.index]

    def next_atom(self):
        tok = self.next()
        if tok.string == '-':
            tok = self.next()
            if tok.type != tokenize.NUMBER:
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))
            return tokenize.TokenInfo(type=tok.type,
                                      string='-' + tok.string,
                                      start=tok.start,
                                      end=tok.end,
                                      line=tok.line)
        return tok

    def peek_atom(self):
        tok = self.peek()
        if tok.string == '-':
            self.next()
            tok = self.peek()
            if tok.type != tokenize.NUMBER:
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))
            return tokenize.TokenInfo(type=tok.type,
                                      string='-' + tok.string,
                                      start=tok.start,
                                      end=tok.end,
                                      line=tok.line)
        return tok

    def parse(self):
        result = []

        while True:
            tok = self.next_atom()

            if tok.type == tokenize.NUMBER:
                item = self.parse_grade(tok)
            elif tok.string == '(':
                item = self.parse_interval()
            else:
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

            tok = self.next_atom()
            if tok.type == tokenize.ENDMARKER:
                if result:
                    result.append(item)
                    return result
                return [item]
            elif tok.string == '|':
                result.append(item)
            else:
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

    def parse_grade(self, number):
        value = float(number.string)
        tok = self.next_atom()
        if tok.type == tokenize.OP and tok.string == '(':
            return Grade(value, self.parse_interval())
        else:
            raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

    def parse_interval(self):
        tok = self.next_atom()

        closed = False
        if tok.type == tokenize.OP and tok.string == '=':
            tok = self.next_atom()
            closed = True

        if tok.type == tokenize.NUMBER:
            left_value = float(tok.string)
            if closed:
                left = lambda x: x >= left_value
            else:
                left = lambda x: x > left_value
            tok = self.next_atom()
            if tok.string != ',':
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))
        elif tok.string == ',':
            left_value = -float('inf')
            left = lambda x: True
        else:
            raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

        tok = self.next_atom()
        if tok.type == tokenize.NUMBER:
            closed_tok = self.peek_atom()
            right_value = float(tok.string)
            if closed_tok.string == '=':
                self.next_atom()
                right = lambda x: x <= right_value
            else:
                right = lambda x: x < right_value

            tok = self.next_atom()
            if tok.string != ')':
                raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

        elif tok.string == ')':
            right_value = float('inf')
            right = lambda x: True
        else:
            raise ParseError('%s unexpected `%s`' % (tok.start, tok.string))

        return Interval(left_value, right_value, left, right)


class Interval(object):
    def __init__(self, left_value, right_value, left, right):
        self.left_value = left_value
        self.right_value = right_value
        self.left = left
        self.right = right

    def in_interval(self, value):
        return self.left(value) and self.right(value)


class Grade(Interval):
    def __init__(self, value, interval):
        self.value = value
        super(Grade, self).__init__(interval.left_value, interval.right_value, interval.left, interval.right)


def amend_volume_unit(volume):
    amend_volume = volume
    if 0 <= volume <= 0.1:
        amend_volume = 0.3
    elif 0.1 < volume <= 0.8:
        amend_volume += 0.2
    elif 0.8 < volume <= 0.9:
        amend_volume += 0.1
    elif 0.9 < volume <= 1:
        amend_volume = 1
    return amend_volume


def amend_trunk_units(volume, weight, volume_deltas, weight_deltas):
    amend_weight_volume = amend_volume_unit(weight * 3.5)
    amend_weight = amend_weight_volume * 0.286
    amend_volume = amend_volume_unit(volume)

#    for volume_delta in Parse(volume_deltas).parse():
#        if volume_delta.in_interval(volume):
#            amend_volume += volume_delta.value
#
#    for weight_delta in Parse(weight_deltas).parse():
#        if weight_delta.in_interval(weight):
#            amend_weight += weight_delta.value

    return amend_volume, amend_weight


def calc_supplier_profit(unit, starting_value, origin_delta, min_delta, delta_variable_regions):
    real_delta_regions = []

    for delta_variable_region in Parse(delta_variable_regions).parse():
        real_delta_regions.append(delta_variable_region)
        if delta_variable_region.in_interval(unit):
            break
    else:
        return 0

    value = starting_value
    delta = origin_delta

    for real_delta_region in real_delta_regions:
        value += delta
        delta = delta + real_delta_region.value if delta >= min_delta else min_delta

    if unit > real_delta_region.left_value and real_delta_region.right_value == float('inf'):
        init = real_delta_region.left_value + 1
        while init < unit:
            value += delta
            delta = delta + real_delta_region.value if delta >= min_delta else min_delta
            init += 1

    if value < starting_value:
        return starting_value

    return value


def calc_ltl_lading_price(unit, milage, min_price_milage, unit_prices, milage_prices):
    if milage <= min_price_milage:
        for milage_price_item in Parse(milage_prices).parse():
            if milage_price_item.in_interval(unit):
                return milage_price_item.value
    else:
        milage_price = 0
        for milage_price_item in Parse(milage_prices).parse():
            if milage_price_item.in_interval(unit):
                milage_price = milage_price_item.value
                break

        for unit_price in Parse(unit_prices).parse():
            if unit_price.in_interval(unit):
                return milage_price + (milage - min_price_milage) * unit_price.value
    return 0


def is_ok_parse(parse: [Grade]):
    if len(parse) == 0:
        raise ParseError('len=0')
    # 交叉对比
    for (x, y) in zip(parse[:-1], parse[1:]):
        if x.in_interval(x.left_value):
            raise ParseError('%s include in %s' % (x.left_value, x))
        if not x.in_interval(x.right_value):
            raise ParseError('%s not include in %s' % (x.right_value, x))
        if x.right_value != y.left_value:
            raise ParseError('%s %s not continuous' % (x, y))
    # 最后是 无穷大
    if parse[-1].right_value != float('inf'):
        raise ParseError('last not inf')


if __name__ == '__main__':
    print(calc_ltl_lading_price(5, 20, 20, Parse(b'1(0,1=)|2(1, 1.5=)|3(1.5,)').parse(),
                                Parse(b'1(0,1=)|2(1, 1.5=)|3(1.5,)').parse()))

    print('1：', calc_supplier_profit(1, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('1.5：', calc_supplier_profit(1.5, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('2：', calc_supplier_profit(2, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('3：', calc_supplier_profit(3, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('4：', calc_supplier_profit(4, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('5：', calc_supplier_profit(5, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('10：', calc_supplier_profit(10, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('20：', calc_supplier_profit(20, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('21：', calc_supplier_profit(21, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('22：', calc_supplier_profit(22, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))
    print('23：', calc_supplier_profit(23, 20, 27, 5, Parse(b'-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))

    # 测试 str
    print('str 23：', calc_supplier_profit(23, 20, 27, 5, Parse('-1(0,1=)|-2(1, 1.5=)|-3(1.5,)').parse()))

    # 测试 '-1(0,1=)|'
    for x in ['', None, b'', '-1(0,1=)|', '-1(0,1)|-2(1, 1.5=)', '-1(0,1=)|-2(1, 1.5)', '-1(0,1=',
              '-1(0,1=)|-2(2,)', '-1(0,1=)|-2(1, 1.)', '-1(=0,1)|-2(1, 1.)', '-1(=0,1=)|-2(1, 1.5=)|-3(1.5,)']:
        try:
            is_ok_parse(Parse(x).parse())
            print('23：', calc_supplier_profit(23, 20, 27, 5, Parse(x).parse()))
        except (ParseError, tokenize.TokenError) as e:
            print('测试 %s ok' % x)
            print(e)
