#!/usr/bin/python3
"""Defines the FileStorage class for file storage."""
import json
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
    """Serializes instances to a JSON file and deserializes back to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects or filtered by class."""
        if cls:
            filtered = {}
            for key, obj in self.__objects.items():
                if isinstance(obj, cls):
                    filtered[key] = obj
            return filtered
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    cls_name = value['__class__']
                    if cls_name in classes:
                        self.__objects[key] = classes[cls_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
