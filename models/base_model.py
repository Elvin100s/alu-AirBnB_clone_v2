#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """Defines the BaseModel class."""
    
    if models.storage_type == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)

    def save(self):
        """Update updated_at with current time and save to storage."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance."""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        my_dict.pop('_sa_instance_state', None)
        return my_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)
