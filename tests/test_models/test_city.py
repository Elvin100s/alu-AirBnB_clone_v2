#!/usr/bin/python3
"""Tests for the City model"""

from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """Unit tests for the City class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test that state_id is a string"""
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """Test that name is a string"""
        new = self.value()
        self.assertEqual(type(new.name), str)
