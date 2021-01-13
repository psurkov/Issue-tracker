from flask import Blueprint, render_template, request, redirect
from app import *
from comment import *

issues = Blueprint('issues', __name__)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    comments = db.relationship('Comment', backref='issue', lazy='dynamic')
    labels = db.relationship('Label', backref='issue', lazy='dynamic')

    def __repr__(self):
        return '<Issue %r>' % self.id

    def title_and_id(self):
        return self.title + ' #' + str(self.id)

    def get_styled_labels(self):
        pass
        # for label in self.labels.all():
        #     print('<div class="' + label.type + '"></div>')


@issues.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        issues = Issue.query.all()
        return render_template('index.html', issues=issues)
    else:
        issue = Issue(title=request.form['title'], author=request.form['author'])
        comment = Comment(text=request.form['text'], issue=issue)
        try:
            db.session.add(issue)
            db.session.add(comment)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"