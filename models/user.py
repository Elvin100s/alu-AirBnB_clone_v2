#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'users'
    
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    
    places = relationship("Place", backref="user", cascade="all, delete-orphan")

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        email = ""
        password = ""
        first_name = ""
        last_name = ""
