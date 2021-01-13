from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from issue import issues as issues_blueprint
from comment import comments as comments_blueprint
from label import labels as labels_blueprint

# def create_app():
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(issues_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(labels_blueprint)
db.init_app(app)

#
#
# if __name__ == '__main__':
#     create_app()

# for label in Issue.query.all()[0].labels.all():
#     print('<div class="' + label.type + '"></div>')
