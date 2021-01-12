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
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Issue %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    print(request.method)
    if request.method == 'GET':
        issues = Issue.query.all()
        return render_template('index.html', issues=issues)
    else:
        issue = Issue(title=request.form['title'], author=request.form['author'], text=request.form['text'])
        try:
            db.session.add(issue)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"

@app.route('/issue/<int:id>')
def issue(id):
    try:
        return render_template('issuepage.html', issue=Issue.query.get(id))
    except:
        return "Error"


if __name__ == '__main__':
    app.run(debug=True)
