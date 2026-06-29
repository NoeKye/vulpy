import sqlite3
import libuser
from werkzeug.security import generate_password_hash, check_password_hash


def login(username, password):
    conn = sqlite3.connect('db_users.sqlite')
    conn.set_trace_callback(print)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    user = c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

    if user:
        return user['username']
    else:
        return False


def create(username, password, salt='', failures=0, mfa_enabled=0, mfa_secret=''):
    conn = sqlite3.connect('db_users.sqlite')
    c = conn.cursor()
    if salt is None:
        salt = ''

    hashed_password = generate_password_hash(password)

    c.execute(
        "INSERT INTO users (username, password, salt, failures, mfa_enabled, mfa_secret) VALUES (?, ?, ?, ?, ?, ?)",
        (username, hashed_password, salt, failures, mfa_enabled, mfa_secret)
    )
    conn.commit()
    conn.close()


def userlist():
    conn = sqlite3.connect('db_users.sqlite')
    conn.set_trace_callback(print)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    users = c.execute("SELECT * FROM users").fetchall()

    if not users:
        return []
    else:
        return [user['username'] for user in users]


def password_change(username, password):
    conn = sqlite3.connect('db_users.sqlite')
    conn.set_trace_callback(print)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    hashed_password = generate_password_hash(password)

    c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))

    conn.commit()
    conn.close()

    return True


def password_complexity(password):
    return True
