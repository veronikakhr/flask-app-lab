from app import db
from datetime import datetime
from enum import Enum as PyEnum


class CategoryEnum(PyEnum):
    """Enum для категорій постів"""
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


class Post(db.Model):
    """Модель для зберігання постів блогу"""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Enum(CategoryEnum), nullable=False, default=CategoryEnum.other)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')
    
    def __repr__(self):
        return f"<Post {self.id}: {self.title} by {self.author}>"