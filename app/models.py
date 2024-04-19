from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    
class User(Base):
    __tablename__="users"
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    id = Column(Integer,primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    