#!/usr/bin/python3
"""Tests for DBStorage"""

import unittest
import models
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not DB storage")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage"""

    def setUp(self):
        self.storage = models.storage

    def tearDown(self):
        del self.storage

    def test_user(self):
        user = User(name="Chyna", email="chyna@gmail.com", password="Chyna12345")
        user.save()
        self.assertIn(f"User.{user.id}", self.storage.all().keys())
        self.assertEqual(user.name, "Chyna")

    def test_city(self):
        state = State(name="California")
        state.save()
        city = City(name="Batch", state_id=state.id)
        city.save()
        self.assertIn(f"City.{city.id}", self.storage.all().keys())
        self.assertEqual(city.name, "Batch")

    def test_state(self):
        state = State(name="California")
        state.save()
        self.assertIn(f"State.{state.id}", self.storage.all().keys())
        self.assertEqual(state.name, "California")

    def test_place(self):
        state = State(name="California")
        state.save()
        city = City(name="Batch", state_id=state.id)
        city.save()
        user = User(name="Chyna", email="chyna@gmail.com", password="Chyna12345")
        user.save()
        place = Place(name="Palace", number_rooms=4, city_id=city.id, user_id=user.id)
        place.save()
        self.assertIn(f"Place.{place.id}", self.storage.all().keys())
        self.assertEqual(place.name, "Palace")

    def test_amenity(self):
        amenity = Amenity(name="Starlink")
        amenity.save()
        self.assertIn(f"Amenity.{amenity.id}", self.storage.all().keys())
        self.assertEqual(amenity.name, "Starlink")

    def test_review(self):
        state = State(name="California")
        state.save()
        city = City(name="Batch", state_id=state.id)
        city.save()
        user = User(name="Chyna", email="chyna@gmail.com", password="Chyna12345")
        user.save()
        place = Place(name="Palace", number_rooms=4, city_id=city.id, user_id=user.id)
        place.save()
        review = Review(text="no comment", place_id=place.id, user_id=user.id)
        review.save()
        self.assertIn(f"Review.{review.id}", self.storage.all().keys())
        self.assertEqual(review.text, "no comment")
