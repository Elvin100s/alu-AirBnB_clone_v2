#!/usr/bin/python3
"""
User Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User class"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)

    password = Column(String(128), nullable=False)

    first_name = Column(String(128), nullable=True)

    last_name = Column(String(128), nullable=True)

    # Relationship with Place for DBStorage
    places = relationship("Place", backref="user",
                         cascade="all, delete-orphan")

    # Relationship with Review for DBStorage
    reviews = relationship("Review", backref="user",
                          cascade="all, delete-orphan")
