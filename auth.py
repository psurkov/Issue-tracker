from flask import Blueprint, render_template, request, redirect
from flask_login import UserMixin, login_user, login_required, logout_user
from sqlalchemy.exc import InvalidRequestError
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
import app

class User(UserMixin, app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String(100), unique=True)
    password = app.db.Column(app.db.String(100))
    name = app.db.Column(app.db.String(100))
    issues = app.db.relationship('Issue', backref='user', lazy='dynamic')
    comments = app.db.relationship('Comment', backref='user', lazy='dynamic')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['inputEmail']
    name = request.form['inputName']
    password = request.form['inputPassword']
    print(email, name, password)

    if User.query.filter_by(email=email).count():  # already exists
        return redirect('/signup')

    user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    try:
        app.db.session.add(user)
        app.db.session.commit()
    except InvalidRequestError:
        return "Error"

    return redirect('/login')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    print(email, password)

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect('/login')
    login_user(user, remember=True)
    return redirect('/')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')