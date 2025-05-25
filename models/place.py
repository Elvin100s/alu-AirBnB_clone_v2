#!/usr/bin/python3
"""Place Module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from os import getenv


<<<<<<< HEAD
# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
                      Column(
                          'place_id',
                          String(60),
                          ForeignKey('places.id'),
                          primary_key=True,
                          nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))
=======
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907


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
    amenity_ids = []

<<<<<<< HEAD
    # For DBStorage
=======
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            "Review",
            backref="place",
<<<<<<< HEAD
            cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates="place_amenities")
=======
            cascade="all, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False
        )
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907
    else:
        @property
        def reviews(self):
            """Get linked Reviews"""
            from models import storage
<<<<<<< HEAD
            review_list = []
            all_reviews = storage.all()
            for obj in all_reviews.values():
                if obj.__class__.__name__ == "Review" and obj.place_id == self.id:
                    review_list.append(obj)
            return review_list
=======
            return [
                obj for obj in storage.all().values()
                if obj.__class__.__name__ == "Review"
                and obj.place_id == self.id
            ]
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907

        @property
        def amenities(self):
            """Get linked Amenities"""
            from models import storage
<<<<<<< HEAD
            amenity_list = []
            all_amenities = storage.all()
            for obj in all_amenities.values():
                if obj.__class__.__name__ == "Amenity" and obj.id in self.amenity_ids:
                    amenity_list.append(obj)
            return amenity_list
=======
            return [
                obj for obj in storage.all().values()
                if obj.__class__.__name__ == "Amenity"
                and obj.id in self.amenity_ids
            ]
>>>>>>> a1a7597a2c04a4f2c17ec7dabcbd2bca01cee907

        @amenities.setter
        def amenities(self, obj):
            """Add Amenity ID to amenity_ids"""
            if obj.__class__.__name__ == "Amenity":
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
