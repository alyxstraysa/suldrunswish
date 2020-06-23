from flask import Flask, session, request, jsonify, render_template, url_for, flash, redirect
from werkzeug.security import check_password_hash
import logging
from forms import LoginForm
from markupsafe import escape
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

from register import RegistrationForm
import os
import pandas as pd
import numpy as np
import psycopg2
import json
import requests
import sys
import pprint

app = Flask(__name__)

if os.environ.get('VIRTUAL_ENV') == '/Users/kitsundere/suldrunswish/venv':
    print("Working locally...")
    from secret import *
    conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                            database=DATABASE, user=USER, password=PASSWORD)
    app.config['SECRET_KEY'] = SECRET_KEY

    print("Login Successful!")
else:
    app.logger.debug("Starting database connection...")
    conn = psycopg2.connect(os.environ.get('DATABASE_URL_KEI'), sslmode='require',
                            database=os.environ.get('DATABASE'), user=os.environ.get('USER'), password=os.environ.get('PASSWORD'))
    app.logger.debug("Database connection successful!")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


class User(UserMixin):
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None
        self.email = None

    def get_id(self):
        return self.username


def user_lookup(username):
    command = (
        """
        SELECT *
        FROM login
        WHERE username = %s
        """
    )

    data = (username,)
    cur = conn.cursor()
    cur.execute(command, data)
    results = cur.fetchone()
    cur.close()

    if results == None:
        print("No user found!")
        return None
    else:
        current_user = {
            "user_id": results[0],
            "username": results[1],
            "password": results[2],
            "email": results[3]
        }
        return current_user


def id_lookup(username):
    command = (
        """
        SELECT *
        FROM login
        WHERE username = %s
        """
    )

    data = (username,)
    cur = conn.cursor()
    cur.execute(command, data)
    results = cur.fetchone()
    cur.close()

    if results == None:
        print("No id found!")
        return None
    else:
        logged_in_user_dict = {
            "user_id": results[0],
            "username": results[1],
            "password": results[2],
            "email": results[3]
        }

        logged_in_user = User()
        logged_in_user.user_id = logged_in_user_dict['user_id']
        logged_in_user.username = logged_in_user_dict['username']
        logged_in_user.password = logged_in_user_dict['password']
        logged_in_user.email = logged_in_user_dict['email']

        return logged_in_user


# Login Logic
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@ login_manager.user_loader
def load_user(user_id):
    user = id_lookup(user_id)
    return user


@ app.route('/')
def index():
    # app.logger.info('this is an INFO message')
    # app.logger.warning('this is a WARNING message')
    # app.logger.error('this is an ERROR message')
    # app.logger.critical('this is a CRITICAL message')
    return render_template('index.html')


@ app.route('/chargen')
def chargen():
    return render_template('chargen.html')


@ app.route('/background')
def background():
    backgrounds = pd.read_csv("static/generators/backstories.csv")
    random_background = backgrounds.loc[np.random.randint(
        len(backgrounds))].iat[0]
    return render_template('background.html', random_background=random_background)


@ app.route('/charlist')
def charlist():
    URL = "https://mysterious-tor-57369.herokuapp.com/api/characters"
    r = requests.get(URL)
    char_list = r.json()
    return render_template('charlist.html', char_list=char_list)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if request.form['action'] == 'changepass':
            return redirect(url_for('changepass'))
        elif request.form['action'] == 'deleteaccount':
            command = (
                """
                DELETE FROM login
                where username = %s;
                """
            )
            cur = conn.cursor()
            data = (current_user.username,)
            cur.execute(command, data)
            cur.close()
            conn.commit()
            logout_user()
            return redirect(url_for('index'))
    return render_template('profile.html')


@app.route('/changepass', methods=['GET', 'POST'])
@login_required
def changepass():
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm']:
            command = (
                """
        UPDATE login
        SET password = %s
        WHERE username = %s
        """
            )

        data = (generate_password_hash(
            request.form['password']), current_user.username)
        cur = conn.cursor()
        cur.execute(command, data)
        cur.close()
        conn.commit()

        logout_user()
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)
    return render_template('changepass.html', form=form)


@ app.route('/example')
def example():
    return render_template('example.html')


@ app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user_dict = user_lookup(username=form.username.data)
        if user_dict is None or (check_password_hash(user_dict['password'], form.password.data) == False):
            print("Invalid username or password!")
            return redirect(url_for('login'))
        user = User()
        user.user_id = user_dict['user_id']
        user.username = user_dict['username']
        user.password = user_dict['password']
        user.email = user_dict['email']
        login_user(user, remember=form.remember_me.data)
        return render_template('profile.html')
    return render_template('login.html', title='Sign In', form=form)


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_pass = generate_password_hash(form.password.data)

        command = (
            """
            INSERT INTO login (username, password, email)
            VALUES (%s, %s, %s);
            """
        )
        data = (form.username.data, hashed_pass, form.email.data)
        cur = conn.cursor()
        cur.execute(command, data)
        cur.close()
        conn.commit()
        print('User added!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    # app.config['DEBUG'] = True
    app.run(threaded=True, port=5000)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
