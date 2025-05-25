#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class User(BaseModel, Base):
    """Representation of a user"""
    if models.storage_type == "db":
        __tablename__ = 'users'
        
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        
        # Relationship with Place - cascade delete when User is deleted
        places = relationship("Place", backref="user", cascade="all, delete-orphan")
        # Relationship with reviews (if you have a Review model)
        # reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
