from flask import Flask, request, jsonify, render_template, url_for
#from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
#db = SQLAlchemy(app)


# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<E-mail %r>' % self.email


# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')


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
