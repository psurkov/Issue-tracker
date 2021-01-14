from flask import Blueprint, render_template, request, redirect
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import *

auth = Blueprint('auth', __name__)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    issues = db.relationship('Issue', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')


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

    db.session.add(user)
    db.session.commit()

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
