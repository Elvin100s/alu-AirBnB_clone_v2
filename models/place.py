#!/usr/bin/python3
"""
Place Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from os import getenv


# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = 'places'
    
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
    
    # For FileStorage
    amenity_ids = []

    # Conditional relationships based on storage type
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity, back_populates="place_amenities")
    
    # FileStorage properties
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Returns list of Review instances with place_id equals to current Place.id"""
            from models import storage
            review_list = []
            all_reviews = storage.all()
            for obj in all_reviews.values():
                if obj.__class__.__name__ == "Review" and obj.place_id == self.id:
                    review_list.append(obj)
            return review_list
        
        @property
        def amenities(self):
            """Returns list of Amenity instances linked to Place"""
            from models import storage
            amenity_list = []
            all_amenities = storage.all()
            for obj in all_amenities.values():
                if obj.__class__.__name__ == "Amenity" and obj.id in self.amenity_ids:
                    amenity_list.append(obj)
            return amenity_list
        
        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities in FileStorage"""
            if obj.__class__.__name__ == "Amenity":
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
