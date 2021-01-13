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
    is_open = db.Column(db.BOOLEAN, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Issue %r>' % self.id

    def title_and_id(self):
        return self.title + ' #' + str(self.id)

    def pretty_date(self):
        return self.timestamp.strftime("%H:%M:%S %b %d %Y")

    def get_styled_labels(self):
        pass
        # for label in self.labels.all():
        #     print('<div class="' + label.type + '"></div>')


def create_index(query, show_open):
    query = query.order_by(Issue.timestamp.desc())
    open_issues = Issue.query.filter_by(is_open=True).count()
    closed_issues = Issue.query.filter_by(is_open=False).count()
    return render_template('index.html', issues=query.all(), open_issues=open_issues, closed_issues=closed_issues,
                           show_open=show_open)


@issues.route('/')
def open_issues():
    return create_index(Issue.query.filter_by(is_open=True), True)


@issues.route('/closed')
def closed_issues():
    return create_index(Issue.query.filter_by(is_open=False), False)


@issues.route('/new-issue', methods=['POST'])
def new_issue():
    issue = Issue(title=request.form['title'], author=request.form['author'])
    comment = Comment(text=request.form['text'], issue=issue)
    db.session.add(issue)
    db.session.add(comment)
    db.session.commit()
    return redirect('/issue/' + str(issue.id))