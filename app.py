from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from forms import RegistrationForm, NameForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, LoginManager, UserMixin, login_user, logout_user
import email_validator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '(SuperSecretKey5000);'
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

bootstrap = Bootstrap(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


# Manually push an application context for database initialization
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/account')
@login_required
def account():
    your_email = current_user.email
    return render_template('account.html', your_email=your_email)


@app.route("/register", methods=['GET', 'POST'])
def register():
    regform = RegistrationForm()
    if regform.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user1 = User.query.filter_by(email=email).first()
        if user1 is None:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            # Here, you would typically insert the data into a database
            flash(f'Account created for {regform.email.data}!', 'success')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=regform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = NameForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user1 = User.query.filter_by(email=email).first()
        if email:
            if user1 and check_password_hash(user1.password_hash, password):
                session['user_id'] = user1.id
                login_user(user1)
                return redirect(url_for('account'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out..')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
def signup():
    return render_template('account.html')


@app.route('/user/<username>')
def user(username):
    return render_template('user.html', name=username)


if __name__ == '__main__':
    app.run(debug=True)