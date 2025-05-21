#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
import json


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        storage._FileStorage__objects = {}

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        storage.new(new)
        obj_dict = storage.all()
        self.assertIn(f'BaseModel.{new.id}', obj_dict)
        self.assertEqual(obj_dict[f'BaseModel.{new.id}'], new)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)
        self.assertIn(f'BaseModel.{new.id}', temp)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))
        with open('file.json', 'r') as f:
            data = json.load(f)
        self.assertIn(f'BaseModel.{new.id}', data)

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            f.write("{}")
        storage.reload()
        self.assertEqual(len(storage.all()), 0)

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        if os.path.exists('file.json'):
            os.remove('file.json')
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        storage.new(new)
        key = f'BaseModel.{new.id}'
        self.assertIn(key, storage.all().keys())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

    def test_delete(self):
        """ Test delete method """
        new = BaseModel()
        storage.new(new)
        storage.save()
        storage.delete(new)
        self.assertNotIn(new, storage.all().values())

    def test_multiple_objects(self):
        """ Test storage with multiple objects """
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()
        storage.save()
        storage.reload()
        self.assertEqual(len(storage.all()), 3)
