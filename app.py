from flask import Flask, session, request, jsonify, render_template, url_for
import logging
from markupsafe import escape
from flask_login import LoginManager, UserMixin
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
    print("Login Successful!")
else:
    conn = psycopg2.connect(os.environ.get('DATABASE_URL_KEI'), sslmode='require',
                            database=os.environ.get('DATABASE'), user=os.environ.get('USER'), password=os.environ.get('PASSWORD'))
    app.logger.debug("Database connection successful!")

# Login Logic
login_manager = LoginManager()
login_manager.init_app(app)


@ login_manager.user_loader
def load_user(user_id):
    return UserMixin.get_id(user_id)


@ app.route('/')
def index():
    app.logger.debug("The environment is heroku: %s",
                     os.environ.get('IS_HEROKU'))
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
    # cur = conn.cursor()
    # cur.execute(
    #    """SELECT * FROM inventory"""
    # )
    # result = cur.fetchall()
    # print(result)

    URL = "https://mysterious-tor-57369.herokuapp.com/api/character"
    r = requests.get(URL)
    char_list = r.json()
    return render_template('charlist.html', char_list=char_list)


@ app.route("/submit", methods=["POST"])
def post_to_db():
    pass


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    # app.config['DEBUG'] = True
    app.run(threaded=True, port=5000)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
