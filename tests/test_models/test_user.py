#!/usr/bin/python3
"""Tests for the User model"""

from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """Unit tests for the User class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Test that first_name is a string"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """Test that last_name is a string"""
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """Test that email is a string"""
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """Test that password is a string"""
        new = self.value()
        self.assertEqual(type(new.password), str)
