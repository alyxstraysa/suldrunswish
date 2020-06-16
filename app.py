from flask import Flask, session, request, jsonify, render_template, url_for
from markupsafe import escape
from flask_login import LoginManager
import os
import pandas as pd
import numpy as np
import psycopg2
import json
import requests
import sys
import flask_login

app = Flask(__name__)


# loginmanager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chargen')
def chargen():
    return render_template('chargen.html')


@app.route('/background')
def background():
    backgrounds = pd.read_csv("static/generators/backstories.csv")
    random_background = backgrounds.loc[np.random.randint(
        len(backgrounds))].iat[0]
    return render_template('background.html', random_background=random_background)


@app.route('/charlist')
def charlist():
    #cur = conn.cursor()
    # cur.execute(
    #    """SELECT * FROM inventory"""
    # )
    #result = cur.fetchall()
    # print(result)

    URL = "https://mysterious-tor-57369.herokuapp.com/api/character"
    r = requests.get(URL)
    char_list = r.json()
    print(char_list)
    sys.stdout.flush()

    return render_template('charlist.html', char_list=char_list)


@app.route("/submit", methods=["POST"])
def post_to_db():
    pass


@app.route('/testpage')
def test_page():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('testpage'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('testpage'))


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    #app.config['DEBUG'] = True
    app.run(threaded=True, port=5000)
