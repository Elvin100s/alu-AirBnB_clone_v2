#!/usr/bin/python3
"""Complete Place implementation"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

class Place(BaseModel, Base):
    """Place class with dual storage support"""
    __tablename__ = 'places'
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initialize Place with storage-appropriate attributes"""
        super().__init__(*args, **kwargs)
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            self.city_id = kwargs.get('city_id', "")
            self.user_id = kwargs.get('user_id', "")
            self.name = kwargs.get('name', "")
            self.description = kwargs.get('description', "")
            self.number_rooms = kwargs.get('number_rooms', 0)
            self.number_bathrooms = kwargs.get('number_bathrooms', 0)
            self.max_guest = kwargs.get('max_guest', 0)
            self.price_by_night = kwargs.get('price_by_night', 0)
            self.latitude = kwargs.get('latitude', 0.0)
            self.longitude = kwargs.get('longitude', 0.0)
            self.amenity_ids = kwargs.get('amenity_ids', [])
