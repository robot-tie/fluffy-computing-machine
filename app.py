from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
import requests

class NameForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Pur2s3cr3t'
bootstrap = Bootstrap(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


def answer():
    res = requests.get('https://example.com')
    return res.headers

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = NameForm()
    result = answer()
    return render_template('login.html', form=form, answer=result)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', name=username)

if __name__ == '__main__':
    app.run(debug=True)