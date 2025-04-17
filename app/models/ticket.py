from datetime import datetime
from app import db

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='abierto')  # abierto, en_progreso, resuelto, cerrado
    priority = db.Column(db.String(20), default='medio')  # bajo, medio, alto, crítico
    category = db.Column(db.String(50))  # hardware, software, red, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    
    # Relaciones
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    
    # Backrefs
    comments = db.relationship('TicketComment', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    
    # Propiedades útiles
    @property
    def is_overdue(self):
        return self.due_date and datetime.utcnow() > self.due_date and self.status not in ['resuelto', 'cerrado']

class TicketComment(db.Model):
    __tablename__ = 'ticket_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_internal = db.Column(db.Boolean, default=False)
    
    # Relaciones
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))