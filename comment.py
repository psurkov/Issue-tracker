from datetime import datetime
from flask import Blueprint, render_template, redirect, request
from app import *
import issue

comments = Blueprint('comments', __name__)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

    def pretty_date(self):
        return self.timestamp.strftime("%H:%M:%S %b %d %Y")


@comments.route('/issue/<int:issue_id>')
def show_issues(issue_id):
    return render_template('issuepage.html', issue=issue.Issue.query.get(issue_id))


@comments.route('/comment/<int:issue_id>', methods=['POST'])
def add_comment(issue_id):
    if not issue.Issue.query.get(issue_id).is_open:
        return "Error"

    comment = Comment(text=request.form['text'], issue=issue.Issue.query.get(issue_id))
    db.session.add(comment)
    db.session.commit()
    if request.form['action'] == 'Comment':
        return redirect('/issue/' + str(issue_id))
    else:
        issue.Issue.query.get(issue_id).is_open = False
        db.session.commit()
        return redirect('/')
