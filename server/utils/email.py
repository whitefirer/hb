# coding=utf-8
# author=whitefirer

from server import log
from server import cache
from server import app

import time
import decimal
from graphviz import Graph, Digraph
import base64

def format_node_data(chart_data, data_type):
    if data_type == 'svg':
        data = chart_data.pipe(format='svg').decode('utf-8')
    elif data_type == 'png':
        png_data = base64.b64encode(chart_data.pipe(format='png')).decode('utf-8')
        data = 'data:image/png;base64,' + png_data
    elif data_type == 'src':
        data = chart_data.source

    return data


def create_node(chart_data, name, label):
    kwargs = {
        'name': str(name),
        'label': str(label),
        'shape': 'none',
        'fontname': 'serif',
        'fontsize': '14',
        'fontcolor': 'black',
    }

    return chart_data.node(**kwargs)

def get_data(payload):

    chart_data = Digraph('邮箱')
    chart_data.graph_attr.update(rank='same', rankdir='TB')
    data_type = 'png'
    emmail = 'whitefirer@gmail.com'

    create_node(chart_data, emmail, emmail)
    
    email_data = format_node_data(chart_data, data_type)
    
    data = {
        'email_data': email_data,
        'data_type': data_type
    }

    return data
