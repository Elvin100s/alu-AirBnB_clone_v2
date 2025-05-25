#!/usr/bin/python3
"""Complete City implementation"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

class City(BaseModel, Base):
    """City class with dual storage support"""
    __tablename__ = 'cities'
    
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        places = relationship("Place", backref="cities", cascade="all, delete-orphan")
    else:
        @property
        def places(self):
            """FileStorage places getter"""
            from models import storage
            return [place for place in storage.all(Place).values() 
                    if place.city_id == self.id]

    def __init__(self, *args, **kwargs):
        """Initialize City"""
        super().__init__(*args, **kwargs)
