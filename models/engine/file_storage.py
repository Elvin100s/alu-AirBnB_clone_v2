#!/usr/bin/python3
"""Test cases for file_storage.py"""
import unittest
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_object(self):
        """Test that new adds an object to storage"""
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

    def test_save_creates_file(self):
        """Test that save creates a file"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload_loads_objects(self):
        """Test that reload loads objects from file"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

    def test_delete_removes_object(self):
        """Test that delete removes an object"""
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.storage.delete(obj)
        self.assertNotIn(key, self.storage.all())

    def test_reload_empty_file(self):
        """Test reload with empty file"""
        with open("file.json", "w") as f:
            f.write("{}")
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    def test_reload_nonexistent_file(self):
        """Test reload with nonexistent file"""
        if os.path.exists("file.json"):
            os.remove("file.json")
        self.assertEqual(self.storage.reload(), None)

    def test_multiple_objects(self):
        """Test storage with multiple objects"""
        objs = [BaseModel() for _ in range(3)]
        for obj in objs:
            self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 3)

if __name__ == '__main__':
    unittest.main()
