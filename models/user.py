#!/usr/bin/python3
"""User class definition"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """User class for database and file storage
    
    Attributes:
        __tablename__ (str): MySQL table name
        email (str): user email
        password (str): user password
        first_name (str): user first name
        last_name (str): user last name
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize User instance"""
        super().__init__(*args, **kwargs)
        if kwargs:
            # Handle both DB and file storage cases
            self.email = kwargs.get('email', "")
            self.password = kwargs.get('password', "")
            self.first_name = kwargs.get('first_name', "")
            self.last_name = kwargs.get('last_name', "")
