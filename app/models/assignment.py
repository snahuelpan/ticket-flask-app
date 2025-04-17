from app import db
from datetime import datetime

# Tabla intermedia para la relación muchos a muchos
assignment_customer = db.Table('assignment_customer',
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.id'), primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.id'), primary_key=True)
)


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # quien hace la entrega
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    asset = db.relationship('Asset', backref='assignments')
    user = db.relationship('User', backref='assignments')
    customers = db.relationship('Customer', secondary=assignment_customer, backref='assignments')
