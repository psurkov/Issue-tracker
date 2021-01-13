from enum import Enum
from flask import Blueprint, redirect
from app import *
import issue


class LabelTypes(Enum):
    BAG = 0
    DOCUMENTATION = 1
    DUPLICATE = 2


labels = Blueprint('labels', __name__)


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(LabelTypes))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))


@labels.route('/issue/<int:issue_id>/add-label/<int:label_id>', methods=['POST'])
def add_label(issue_id, label_id):
    try:
        label_type = LabelTypes(label_id)
    except ValueError:
        return "Error"
    print(label_type)

    label = Label(type=label_type, issue=issue.Issue.query.get(issue_id))
    try:
        db.session.add(label)
        db.session.commit()
        return redirect('/issue/' + str(issue_id))
    except:
        return "Error"