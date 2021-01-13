import secrets
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from auth import auth as auth_blueprint
from issue import issues as issues_blueprint
from comment import comments as comments_blueprint
from label import labels as labels_blueprint

from auth import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.register_blueprint(auth_blueprint)
app.register_blueprint(issues_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(labels_blueprint)
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# with app.app_context():
#     db.create_all()


#
#
# if __name__ == '__main__':
#     create_app()

# for label in Issue.query.all()[0].labels.all():
#     print('<div class="' + label.type + '"></div>')
