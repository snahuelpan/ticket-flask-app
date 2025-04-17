from datetime import datetime
from app import db

return_customer = db.Table('return_customer',
    db.Column('return_id', db.Integer, db.ForeignKey('return.id'), primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True)
)


class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    returned_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    assignment = db.relationship('Assignment', backref='returns')
    user = db.relationship('User', backref='returns')
    customers = db.relationship('Customer', secondary=return_customer, backref='returns')
