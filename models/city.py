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
<<<<<<< HEAD

    places = relationship(
        "Place",
        backref="cities",
        cascade="all, delete-orphan")
=======
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907

    places = relationship("Place", backref="cities",
                         cascade="all, delete-orphan")
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        state_id = ""
        name = ""
