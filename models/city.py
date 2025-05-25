#!/usr/bin/python3
"""This module defines a class City"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models


class City(BaseModel, Base):
    """Representation of City"""
    if models.storage_type == "db":
        __tablename__ = 'cities'
        
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        
        # Relationship with Place - cascade delete when City is deleted
        places = relationship("Place", backref="cities", cascade="all, delete-orphan")
    else:
        state_id = ""
        name = ""

    @property
    def places(self):
        """Getter attribute that returns the list of Place instances with
        city_id equals to the current City.id
        FileStorage relationship between City and Place
        """
        if models.storage_type != "db":
            place_list = []
            all_places = models.storage.all("Place")
            for place in all_places.values():
                if place.city_id == self.id:
                    place_list.append(place)
            return place_list
