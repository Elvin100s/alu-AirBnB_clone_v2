#!/usr/bin/python3
"""User class with complete functionality"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class User(BaseModel, Base):
    """User class with dual storage support"""
    __tablename__ = 'users'
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize User with storage-appropriate attributes"""
        super().__init__(*args, **kwargs)
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.email = kwargs.get('email', "")
            self.password = kwargs.get('password', "")
            self.first_name = kwargs.get('first_name', "")
            self.last_name = kwargs.get('last_name', "")
