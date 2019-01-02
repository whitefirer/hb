# coding=utf-8
# author=whitefirer

from server import log
from server import cache
from server import app

import time
import decimal
from graphviz import Graph, Digraph
import base64
from .crypt import Crypt

def get_hit_count(key):
    retries = 5

    while True:
        try:
            return cache.incr(key)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

    return 0

to_child_edge = {
    'color': 'slateblue',
    'penwidth': '1',
    'arrowsize': '0.8',
}

def create_tips(chart_data, tip, name='0'):
    kwargs = {
        'name': name,
        'label': tip,
        'tooltip': 'Happy 2019~',
        'shape': 'note',
        'color': 'grey',
        'fillcolor': 'khaki1',
        'style': 'filled',
        'fontsize': '10',
        'fontcolor': 'red',
        'penwidth': '0.5',
    }

    if not tip:
        kwargs.update({
            #'width': '0',
            'style': 'invis',
        })

    return chart_data.node(**kwargs)

def create_node(chart_data, name, label):
    kwargs = {
        'name': str(name),
        'label': str(label),
        'tooltip': 'Happy 2019~',
        'shape': 'ellipse',
        'color': 'lightblue2',
        'style': 'filled',
        'fontsize': '10',
        'fontcolor': 'black',
    }

    return chart_data.node(**kwargs)

def create_nodes(chart_data, nodes, col, cpt=None):
    if col == 0:
        return 

    new_nodes = []
    for node in nodes:
        left_node = node*2
        right_node = left_node + 1
        new_nodes += [left_node, right_node]
        node_name = cpt.encrypt(str(node)) if (cpt and node != 1) else str(node)
        left_name = cpt.encrypt(str(left_node)) if cpt else str(left_node)
        right_name = cpt.encrypt(str(right_node)) if cpt else str(right_node)

        create_node(chart_data, node_name, node)
        create_node(chart_data, left_name, left_node)
        create_node(chart_data, right_name, right_node)
        chart_data.edge(node_name, left_name, **to_child_edge)
        chart_data.edge(node_name, right_name, **to_child_edge)

    return create_nodes(chart_data, new_nodes, col-1, cpt)

def format_node_data(chart_data, data_type):
    if data_type == 'svg':
        node_data = chart_data.pipe(format='svg').decode('utf-8')
    elif data_type == 'png':
        png_data = base64.b64encode(chart_data.pipe(format='png')).decode('utf-8')
        node_data = 'data:image/png;base64,' + png_data
    elif data_type == 'src':
        node_data = chart_data.source

    return node_data

def create_hb201901(chart_data, node_id, click_time):
    answer = bytes(app.config['HB201901_CODE'], 'utf-8')
    answer_tip = 'I also want to know'
    question_tip = '2**73+37 is a prime number?'
    failed_tip = '胜败乃兵家常事，少侠请从头再来'
    tips = {
        '-1' : '好疼啊',
        '0' : '点疼我了~',
        '1' : '2019新年快乐！\n难度：Easy',
        '2' : '2是第一个素数',
        '16': 'AES的16位key是什么？',
        '37': '答案的关键',
        '73': '谢耳朵最喜欢的数字',
        '2019': '新年快乐~',
        '9102': '我有一个疑问\n需要2019解答',
        '9444732965739290427429': '恭喜你找到了！'
    }
    #log.debug('hb201901 tips: %s' % tips)

    tip = tips.get(str(node_id))

    try:
        click_time = '%10.06f' % click_time
        secret_key = click_time.replace('.', '')
        log.debug('Crypt secret_key: %s' % secret_key)
        node_id = int(node_id)
        create_node(chart_data, node_id, node_id)
    except Exception as e:
        log.error(str(e))
        node_id = 1
        tip = failed_tip

    if tip:
        name = '0'
        if node_id == 2019:
            cpt = Crypt(secret_key)
            name = cpt.encrypt(answer_tip)
        if node_id == 9102:
            cpt = Crypt(secret_key)
            name = cpt.encrypt(question_tip)
        elif node_id == 9444732965739290427429: # 2**73+37
            cpt = Crypt(secret_key)
            name = cpt.encrypt(base64.b64encode(answer).decode('utf-8'))
        create_tips(chart_data, tip, name)
        log.debug('create_hb201901 tip:%s' % tip)

    if node_id > 0:
        create_nodes(chart_data, [int(node_id)], 3)

    if tip == failed_tip:
        return False
    
    return True

def create_hb201902(chart_data, node_id, click_time):
    answer = bytes(app.config['HB201902_CODE'], 'utf-8')
    failed_tip = '胜败乃兵家常事，少侠请从头再来'
    tips = {
        '0' : '点得我好疼啊~',
        '1' : '送分题\n难度：未知',
        '2' : '2是第一个素数',
        '16': 'AES的16位key是什么？',
        '37': '答案的关键',
        '73': '谢耳朵最喜欢的数字',
        '2019': '新年快乐~',
        '9102': '2019有你想有的东西',
        '9444732965739290427429': '恭喜你找到了！\n'
    }
    #log.debug('hb201902 tips: %s' % tips)

    tip = ''
    max_try = 30
    try:
        try_cnt = get_hit_count('#'.join(['201902', str(click_time)]))
        log.debug('try_cnt: %d' % try_cnt)
        if try_cnt > max_try: # 30次
            node_id = '1'
            tip = failed_tip
    except Exception as e:
        log.error('try_cnt: %s' % str(e))
        node_id = '1'
        tip = 'redis stopped'

    cpt = None
    try:
        if node_id not in ['-1','0', '1']:
            old_secret_key = ('%10.06f' % (click_time+20190101+try_cnt-1)).replace('.', '')
            log.debug('Crypt old_secret_key: %s' % old_secret_key)
            cpt = Crypt(old_secret_key)
            try:
                node_id = cpt.decrypt(node_id)
            except Exception as e:
                node_id = '0'

        if tip in [failed_tip, 'redis stopped']:
            try_cnt = 0
            click_time = float('%10.06f' % time.time())
        secret_key = ('%10.06f' % (click_time+20190101+try_cnt)).replace('.', '')
        log.debug('Crypt secret_key: %s' % secret_key)
        cpt = Crypt(secret_key)

    except Exception as e:
        log.error('Crypt: %s' % str(e))
        node_id = '1'
        tip = failed_tip

    log.debug("create_hb201902 node_id: %s" % node_id)

    if tip not in [failed_tip, 'redis stopped']:
        tip = tips.get(str(node_id))

    create_tips(chart_data, '剩余步数%s' % (max_try-try_cnt), '-1')
    name = '0'
    if tip:
        tip_secret_key = ('%10.06f' % click_time).replace('.', '')
        tip_cpt = Crypt(tip_secret_key)
        if node_id == '2019':
            name = tip_cpt.encrypt('the old place')
        elif node_id == '9444732965739290427429': # 2**73+37
            name = tip_cpt.encrypt(base64.b64encode(answer).decode('utf-8'))
    create_tips(chart_data, tip, name)
    log.debug('create_hb201902 tip:%s' % tip)
    
    if node_id not in ['0', '-1']:
        create_nodes(chart_data, [int(node_id)], 3, cpt)

    if tip in [failed_tip, 'redis stopped']:
        return False, click_time
    
    return True, click_time

def get_data(payload):
    node_id = payload.get('node_id')
    hb_id = payload.get('hb_id')
    click_time = payload.get('click_time')

    data_type = 'src'
    node_data = ''

    chart_data = Digraph('红包'+str(hb_id))
    chart_data.graph_attr.update(rank='same', rankdir='TB')

    if hb_id == '201901':
        click_time = float('%10.06f' % click_time)
        ret = create_hb201901(chart_data, node_id, click_time)
    elif hb_id == '201902':
        ret, click_time = create_hb201902(chart_data, node_id, click_time)
    
    node_data = format_node_data(chart_data, data_type)
    
    data = {
        'click_time': click_time,
        'node_id': payload.get('node_id'),
        "hb_id": payload.get('hb_id'),
        'node_data': node_data,
        'data_type': data_type
    }

    return data
