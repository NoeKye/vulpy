import sqlite3
from flask import Blueprint, render_template, redirect, request, g, abort

import libposts
import libuser

mod_posts = Blueprint('mod_posts', __name__, template_folder='templates')


@mod_posts.route('/')
@mod_posts.route('/<username>')
def do_view(username=None):

    if not username:
        if 'username' in g.session:
            username = g.session['username']
        else:
            return redirect('/user/login')
    current_logged_in_user = g.session.get('username')

    if username != current_logged_in_user:
        return abort(403)

    posts = libposts.get_posts(username)
    users = libuser.userlist()

    return render_template('posts.view.html', posts=posts, username=username, users=users)


@mod_posts.route('/', methods=['POST'])
def do_create():

    if 'username' not in g.session:
        return redirect('/user/login')

    if request.method == 'POST':

        username = g.session['username']
        text = request.form.get('text')

        libposts.post(username, text)

    return redirect('/')

