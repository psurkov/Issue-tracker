from datetime import datetime
from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from sqlalchemy.exc import InvalidRequestError

from app import *
import issue

comments = Blueprint('comments', __name__)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

    def pretty_date(self):
        return self.timestamp.strftime("%H:%M:%S %b %d %Y")


@comments.route('/issue/<int:issue_id>')
def show_issues(issue_id):
    return render_template('issuepage.html', issue=issue.Issue.query.get(issue_id))


@comments.route('/comment/<int:issue_id>', methods=['POST'])
@login_required
def add_comment(issue_id):
    if not issue.Issue.query.get(issue_id).is_open:
        return "Error"

    comment = Comment(text=request.form['text'], issue=issue.Issue.query.get(issue_id), user=current_user)
    print(current_user)
    try:
        db.session.add(comment)
        db.session.commit()
    except InvalidRequestError:
        return "Error"

    if request.form['action'] == 'Comment':
        return redirect('/issue/' + str(issue_id))
    else:
        issue.Issue.query.get(issue_id).is_open = False
        try:
            db.session.commit()
        except InvalidRequestError:
            return "Error"
        return redirect('/')
