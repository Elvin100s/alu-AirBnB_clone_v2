#!/usr/bin/python3
"""This module defines a class City"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of City"""
    __tablename__ = 'cities'
    
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    
    # Relationship with Place - cascade delete when City is deleted
    places = relationship("Place", backref="cities", cascade="all, delete-orphan")
