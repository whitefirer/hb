# coding=utf-8
# author=whitefirer

"""
主页渲染模块

"""

from server import app, log
from flask import Flask, request, render_template, Markup, session, jsonify, redirect
from flask import abort, url_for, jsonify, g
import json
import urllib.parse
import datetime

@app.route('/index/')
def index():
    return render_template('index.html')