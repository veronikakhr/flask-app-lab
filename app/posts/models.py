from app import db
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, DateTime, Enum


class CategoryEnum(PyEnum):
    """Enum для категорій постів"""
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


class Post(db.Model):
    """Модель для зберігання постів блогу (синтаксис SA 2.0)"""
    
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    posted: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    
    category: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum), 
        nullable=False, 
        default=CategoryEnum.other
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    author: Mapped[str] = mapped_column(String(20), default='Anonymous')
        
    def __repr__(self):
        return f"<Post {self.id}: {self.title} by {self.author}>"