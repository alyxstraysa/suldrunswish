from flask import Flask, request, jsonify, render_template, url_for
#from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import numpy as np
import psycopg2
from tables import create_tables, edit_tables, add_inventory
import json
import requests
import sys

# create_tables(conn)
# edit_tables(conn)
# add_inventory(conn)
app = Flask(__name__)


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

    URL = "https://mysterious-tor-57369.herokuapp.com/api/1"
    r = requests.get(URL)
    char_list = r.json()
    print(char_list)
    sys.stdout.flush()

    return render_template('charlist.html', char_list=char_list)


@app.route("/submit", methods=["POST"])
def post_to_db():
    pass


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    #app.config['DEBUG'] = True
    app.run(threaded=True, port=5000)
