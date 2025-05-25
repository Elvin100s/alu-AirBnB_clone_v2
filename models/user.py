#!/usr/bin/python3
"""This module defines the User class for the AirBnB clone project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class User(BaseModel, Base):
    """This class defines a user by various attributes for SQLAlchemy
    
    Attributes:
        __tablename__ (str): The name of the MySQL table to store users
        email (sqlalchemy.String): The email address of the user
        password (sqlalchemy.String): The password of the user
        first_name (sqlalchemy.String): The first name of the user
        last_name (sqlalchemy.String): The last name of the user
        places (sqlalchemy.relationship): Relationship with Place class
        reviews (sqlalchemy.relationship): Relationship with Review class
    """
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
        """Initializes a User instance"""
        super().__init__(*args, **kwargs)
