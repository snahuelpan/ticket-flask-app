from app import db
from datetime import datetime

class KnowledgeBaseArticle(db.Model):
    __tablename__ = 'knowledge_base_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    keywords = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relación con el autor
    author = db.relationship('User', backref='knowledge_base_articles')
    
    def __repr__(self):
        return f'<KnowledgeBaseArticle {self.id}: {self.title}>'