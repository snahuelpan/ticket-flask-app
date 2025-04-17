from app import db
from flask import current_app
import requests
from sqlalchemy import Column, Integer, text

class CostCenter(db.Model):
    __tablename__ = 'cost_center'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300), index= True, unique=True)
    name = db.Column(db.String(64), index=True , unique=True)
    id_number = db.Column(db.Integer, unique=True)
    branch = db.Column(db.String(300))
    location = db.Column(db.String(300) , nullable=True)
    management=db.Column(db.String(300))
    manager = db.Column(db.String(300))
    email_manager = db.Column(db.String(120))
    administrator = db.Column(db.String(300))
    administrator_email = db.Column(db.String(300))
    administrator_cellphone = db.Column(db.String(16))
    active = db.Column(db.Integer , server_default=text("1"))

    def __repr__(self):
        return f'<Cost Center {self.name} {self.id_number}>'
    
     # Flask-Login requiere estos métodos:
    def get_id(self):
        return str(self.uuid)
    
    @property
    def is_active(self):
        return self.active
    
    