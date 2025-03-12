from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.authors_database import authors_base

# authors database
class User(authors_base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    login = Column(String, unique=True, index=True)
    
    # создание связей с таблицами Post и Blog для запросов
    blogs = relationship('Blog', back_populates='owner')
    posts = relationship('Post', back_populates='author')

    
class Blog(authors_base): 
    __tablename__ = 'blog'
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    description = Column(String)
    
    owner = relationship('User', back_populates='blogs')
    posts = relationship('Post', back_populates='blog')
    
class Post(authors_base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    text = Column(String)
    author_id = Column(Integer, ForeignKey('user.id'))
    blog_id = Column(Integer, ForeignKey('blog.id'))
    
    author = relationship('User', back_populates='posts')
    blog = relationship('Blog', back_populates='posts')
    
    
