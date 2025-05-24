#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Place': Place,
    'Amenity': Amenity,
    'Review': Review
}

class FileStorage:
    """Serializes instances to JSON file and deserializes back"""
    
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns dictionary of all objects or filtered by class"""
        if cls:
            return {k: v for k, v in self.__objects.items() 
                   if isinstance(v, cls)}
        return self.__objects.copy()

    def new(self, obj):
        """Adds object to __objects dictionary"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to JSON file"""
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserializes JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    cls_name = value['__class__']
                    if cls_name in classes:
                        obj = classes[cls_name](**value)
                        # Handle datetime attributes
                        if 'created_at' in value:
                            obj.created_at = datetime.strptime(
                                value['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                        if 'updated_at' in value:
                            obj.updated_at = datetime.strptime(
                                value['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                        self.__objects[key] = obj
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls reload() method"""
        self.reload()
