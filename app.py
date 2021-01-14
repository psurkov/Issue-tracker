import secrets
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import auth
import issue
import comment
import label

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.register_blueprint(auth.auth)
app.register_blueprint(issue.issues)
app.register_blueprint(comment.comments)
app.register_blueprint(label.labels)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return auth.User.query.get(int(user_id))


with app.app_context():
    db.create_all()
