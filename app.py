from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='issue', lazy='dynamic')

    def __repr__(self):
        return '<Issue %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))


@app.route('/', methods=['POST', 'GET'])
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


@app.route('/comment/<int:issue_id>', methods=['POST'])
def add_comment(issue_id):
    comment = Comment(text=request.form['text'], issue=Issue.query.get(issue_id))
    try:
        db.session.add(comment)
        db.session.commit()
        return redirect('/')
    except:
        return "Error"


if __name__ == '__main__':
    app.run(debug=True)
