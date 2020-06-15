from flask import Flask, request, jsonify, render_template, url_for
#from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import numpy as np
import psycopg2
from tables import create_tables

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


@app.route('/example')
def example():
    return render_template('example.html')


@app.route("/submit", methods=["POST"])
def post_to_db():
    pass


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    #app.config['DEBUG'] = True
    app.run(threaded=True, port=5000)
