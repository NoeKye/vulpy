#!/usr/bin/env python3

from pathlib import Path

from flask import Flask, g, redirect, request

import libsession
from mod_api import mod_api
from mod_csp import mod_csp
from mod_hello import mod_hello
from mod_mfa import mod_mfa
from mod_posts import mod_posts
from mod_user import mod_user
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("vulpy.main")
logger.info("Ứng dụng Vulpy đã khởi chạy thành công với hệ thống Logging an toàn.")
app = Flask('vulpy')
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Chuoi_Ngau_Nhien_Sieu_Dai_Va_An_Toan_123!')

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')
app.register_blueprint(mod_csp, url_prefix='/csp')
app.register_blueprint(mod_api, url_prefix='/api')

csp_file = Path('csp.txt')
csp = ''

if csp_file.is_file():
    with csp_file.open() as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line = line.replace('\n', '')
            if line:
                csp += line
if csp:
    print('CSP:', csp)


@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

@app.after_request
def add_csp_headers(response):
    if csp:
        response.headers['Content-Security-Policy'] = csp
    return response


app.run(host='127.0.0.1', port=5000, debug=False) #nosemgrep
