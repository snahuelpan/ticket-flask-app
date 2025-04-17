from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, text

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300), index= True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    active = db.Column(db.Integer , server_default=text("1"))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        print(password)
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
     # Flask-Login requiere estos métodos:
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_anonymous(self):
        return False