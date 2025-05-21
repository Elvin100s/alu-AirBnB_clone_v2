#!/usr/bin/python3
"""Defines the BaseModel class that all other classes will inherit from."""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Set up SQLAlchemy Base if using DB storage
if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """The BaseModel class from which all other classes will inherit"""
    
    if models.storage_type == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    # Handle both string and datetime inputs
                    if isinstance(value, str):
                        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)
                elif key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """String representation of the BaseModel instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time and saves to storage"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        
        # Remove SQLAlchemy-specific attribute if it exists
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
            
        return new_dict

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
