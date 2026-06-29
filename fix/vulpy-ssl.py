#!/usr/bin/env python3

from flask import Flask, g, redirect, request

from mod_hello import mod_hello
from mod_user import mod_user
from mod_posts import mod_posts
from mod_mfa import mod_mfa

import libsession
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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'S3cur3_R4nd0m_Fl4sk_K3y_SSL_987654321!')

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')


@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

app.run(debug=False, host='127.0.0.1', ssl_context=('acme.cert', 'acme.key'))