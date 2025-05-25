#!/usr/bin/python3
"""This module defines a class City"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """Representation of City"""
    __tablename__ = 'cities'

    
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    places = relationship(
        "Place",
        backref="cities",
        cascade="all, delete-orphan"
    )

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        state_id = ""
        name = ""


# Two blank lines after class definition
