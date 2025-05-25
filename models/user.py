#!/usr/bin/python3
"""User class implementation for AirBnB clone"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """User class that represents a user in the system
    
    Attributes:
        __tablename__ (str): MySQL table name
        email (sqlalchemy.String): user's email (required, max 128 chars)
        password (sqlalchemy.String): user's password (required, max 128 chars)
        first_name (sqlalchemy.String): optional first name (max 128 chars)
        last_name (sqlalchemy.String): optional last name (max 128 chars)
    """
    __tablename__ = 'users'
    
    # Database columns (always defined for SQLAlchemy)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    
    # Relationships
    places = relationship("Place", backref="user", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        """Initialize User instance"""
        # For file storage, set default values
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.email = ""
            self.password = ""
            self.first_name = ""
            self.last_name = ""
        
        # Call parent constructor
        super().__init__(*args, **kwargs)
