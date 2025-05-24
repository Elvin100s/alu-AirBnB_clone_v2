#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """The BaseModel class that other classes will inherit from"""
    
    if models.storage_type == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes base model with proper attribute validation"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            try:
                # Handle datetime conversion
                if 'created_at' in kwargs:
                    kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                if 'updated_at' in kwargs:
                    kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                
                # Set attributes with validation
                for key, value in kwargs.items():
                    if key != '__class__':
                        if not hasattr(self, key) and key not in self.__dict__:
                            raise KeyError(f"Invalid attribute: {key}")
                        setattr(self, key, value)
            except ValueError as e:
                raise ValueError("Incorrect datetime format") from e

    def __str__(self):
        """String representation of the instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at and saves to storage"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        new_dict.pop('_sa_instance_state', None)
        return new_dict

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)
