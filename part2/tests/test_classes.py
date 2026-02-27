#!/usr/bin/python3
"""Unit tests for User model."""

import unittest
import time
from datetime import datetime

from app import create_app
from app.services import facade
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class TestUserCreate(unittest.TestCase):
    """Tests for User creation."""

    # ----------------------------
    # Basic creation / BaseModel
    # ----------------------------
    def test_create_valid_user(self):
        """Create user with valid fields."""
        u = User("John", "Doe", "john.doe@example.com")
        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertIsInstance(u.updated_at, datetime)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "john.doe@example.com")
        self.assertFalse(u.is_admin)

    # ----------------------------
    # first_name validation
    # ----------------------------
    def test_first_name_type_error(self):
        """Reject non-string first_name."""
        with self.assertRaises(TypeError):
            User(123, "Doe", "john.doe@example.com")

    def test_first_name_required_empty(self):
        """Reject empty first_name."""
        with self.assertRaises(ValueError):
            User("", "Doe", "john.doe@example.com")

    def test_first_name_required_spaces(self):
        """Reject blank first_name."""
        with self.assertRaises(ValueError):
            User("   ", "Doe", "john.doe@example.com")

    def test_first_name_strips(self):
        """Strip first_name spaces."""
        u = User("  John  ", "Doe", "john.doe@example.com")
        self.assertEqual(u.first_name, "John")

    def test_first_name_max_len_50_ok(self):
        """Accept first_name length 50."""
        name = "a" * 50
        u = User(name, "Doe", "john.doe@example.com")
        self.assertEqual(u.first_name, name)

    def test_first_name_len_51_rejected(self):
        """Reject first_name length > 50."""
        with self.assertRaises(ValueError):
            User("a" * 51, "Doe", "john.doe@example.com")

    # ----------------------------
    # last_name validation
    # ----------------------------
    def test_last_name_type_error(self):
        """Reject non-string last_name."""
        with self.assertRaises(TypeError):
            User("John", None, "john.doe@example.com")

    def test_last_name_required_empty(self):
        """Reject empty last_name."""
        with self.assertRaises(ValueError):
            User("John", "", "john.doe@example.com")

    def test_last_name_required_spaces(self):
        """Reject blank last_name."""
        with self.assertRaises(ValueError):
            User("John", "   ", "john.doe@example.com")

    def test_last_name_strips(self):
        """Strip last_name spaces."""
        u = User("John", "  Doe  ", "john.doe@example.com")
        self.assertEqual(u.last_name, "Doe")

    def test_last_name_max_len_50_ok(self):
        """Accept last_name length 50."""
        name = "b" * 50
        u = User("John", name, "john.doe@example.com")
        self.assertEqual(u.last_name, name)

    def test_last_name_len_51_rejected(self):
        """Reject last_name length > 50."""
        with self.assertRaises(ValueError):
            User("John", "b" * 51, "john.doe@example.com")

    # ----------------------------
    # email validation
    # ----------------------------
    def test_email_type_error(self):
        """Reject non-string email."""
        with self.assertRaises(TypeError):
            User("John", "Doe", 42)

    def test_email_required_empty(self):
        """Reject empty email."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "")

    def test_email_required_spaces(self):
        """Reject blank email."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "   ")

    def test_email_reject_internal_spaces(self):
        """Reject email with spaces."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "john doe@example.com")

    def test_email_strips_and_lower(self):
        """Strip and lowercase email."""
        u = User("John", "Doe", "  JOHN.DOE@EXAMPLE.COM  ")
        self.assertEqual(u.email, "john.doe@example.com")

    def test_email_missing_at_rejected(self):
        """Reject email missing @."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "john.doeexample.com")

    def test_email_missing_local_rejected(self):
        """Reject email missing local part."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "@example.com")

    def test_email_missing_domain_rejected(self):
        """Reject email missing domain."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "john.doe@")

    def test_email_missing_tld_dot_rejected(self):
        """Reject email missing dot tld."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "john.doe@example")

    def test_email_accept_subdomain(self):
        """Accept email with subdomain."""
        u = User("John", "Doe", "john.doe@mail.example.co.uk")
        self.assertEqual(u.email, "john.doe@mail.example.co.uk")

    # ----------------------------
    # is_admin validation
    # ----------------------------
    def test_is_admin_type_error(self):
        """Reject non-bool is_admin."""
        with self.assertRaises(TypeError):
            User("John", "Doe", "john.doe@example.com", is_admin="yes")

    def test_is_admin_true_ok(self):
        """Accept is_admin True."""
        u = User("John", "Doe", "john.doe@example.com", is_admin=True)
        self.assertTrue(u.is_admin)


class TestUserUpdate(unittest.TestCase):
    """Tests for User update method."""

    def setUp(self):
        """Create a user for update tests."""
        self.u = User("John", "Doe", "john.doe@example.com")

    # ----------------------------
    # update basics
    # ----------------------------
    def test_update_requires_dict(self):
        """Reject non-dict update payload."""
        with self.assertRaises(TypeError):
            self.u.update(["email", "x@y.com"])

    def test_update_empty_dict_no_change(self):
        """Empty update does not change updated_at."""
        old = self.u.updated_at
        self.u.update({})
        self.assertEqual(self.u.updated_at, old)

    # ----------------------------
    # update first_name
    # ----------------------------
    def test_update_first_name_ok(self):
        """Update first_name updates timestamp."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({"first_name": "  Morgane  "})
        self.assertEqual(self.u.first_name, "Morgane")
        self.assertGreater(self.u.updated_at, old)

    def test_update_first_name_invalid(self):
        """Reject invalid first_name update."""
        old_name = self.u.first_name
        old_time = self.u.updated_at
        with self.assertRaises(ValueError):
            self.u.update({"first_name": "   "})
        self.assertEqual(self.u.first_name, old_name)
        self.assertEqual(self.u.updated_at, old_time)

    # ----------------------------
    # update last_name
    # ----------------------------
    def test_update_last_name_ok(self):
        """Update last_name updates timestamp."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({"last_name": "  Abbattista  "})
        self.assertEqual(self.u.last_name, "Abbattista")
        self.assertGreater(self.u.updated_at, old)

    # ----------------------------
    # update email
    # ----------------------------
    def test_update_email_ok(self):
        """Update email normalizes and updates timestamp."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({"email": "  NEW@EXAMPLE.COM  "})
        self.assertEqual(self.u.email, "new@example.com")
        self.assertGreater(self.u.updated_at, old)

    def test_update_email_invalid_rejected(self):
        """Reject invalid email update."""
        old_email = self.u.email
        old_time = self.u.updated_at
        with self.assertRaises(ValueError):
            self.u.update({"email": "lol"})
        self.assertEqual(self.u.email, old_email)
        self.assertEqual(self.u.updated_at, old_time)

    # ----------------------------
    # update is_admin
    # ----------------------------
    def test_update_is_admin_ok(self):
        """Update is_admin updates timestamp."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({"is_admin": True})
        self.assertTrue(self.u.is_admin)
        self.assertGreater(self.u.updated_at, old)

    def test_update_is_admin_invalid(self):
        """Reject invalid is_admin update."""
        old_val = self.u.is_admin
        old_time = self.u.updated_at
        with self.assertRaises(TypeError):
            self.u.update({"is_admin": "true"})
        self.assertEqual(self.u.is_admin, old_val)
        self.assertEqual(self.u.updated_at, old_time)

    # ----------------------------
    # update unknown/protected
    # ----------------------------
    def test_update_ignores_unknown_keys(self):
        """Unknown keys do not change timestamp."""
        old = self.u.updated_at
        self.u.update({"unknown": "x"})
        self.assertEqual(self.u.updated_at, old)

    def test_update_blocks_id_change(self):
        """Ignore attempts to change id."""
        old_id = self.u.id
        old_time = self.u.updated_at
        self.u.update({"id": "hack"})
        self.assertEqual(self.u.id, old_id)
        self.assertEqual(self.u.updated_at, old_time)


class TestReviewModelRelations(unittest.TestCase):
    """Model-level tests for Review relations to User and Place."""

    def test_review_accepts_valid_user_and_place(self):
        """Create review with valid linked User and Place instances."""
        owner = User("Owner", "User", "owner.model@example.com")
        reviewer = User("Review", "User", "review.model@example.com")
        place = Place(
            title="Model Place",
            description="Place for model relation test",
            price=120,
            latitude=10,
            longitude=20,
            owner=owner,
        )

        review = Review(
            text="Great stay",
            rating=5,
            place=place,
            user=reviewer,
        )

        self.assertIs(review.place, place)
        self.assertIs(review.user, reviewer)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, "Great stay")

    def test_review_rejects_invalid_place_relation(self):
        """Reject review creation when place is not a Place instance."""
        reviewer = User("Review", "User", "review.invalid.place@example.com")
        with self.assertRaises(TypeError):
            Review(
                text="Invalid place relation",
                rating=4,
                place="not-a-place",
                user=reviewer,
            )

    def test_review_rejects_invalid_user_relation(self):
        """Reject review creation when user is not a User instance."""
        owner = User("Owner", "User", "owner.invalid.user@example.com")
        place = Place(
            title="Another Place",
            description="Place for invalid user relation test",
            price=80,
            latitude=5,
            longitude=5,
            owner=owner,
        )

        with self.assertRaises(TypeError):
            Review(
                text="Invalid user relation",
                rating=4,
                place=place,
                user="not-a-user",
            )


class TestUserEndpoints(unittest.TestCase):
    """Tests for User API endpoints."""

    def setUp(self):
        """Create app test client and isolate in-memory user storage."""
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()

    def test_create_user(self):
        """Create user with valid payload returns 201."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "Jane")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "jane.doe@example.com")

    def test_create_user_invalid_data(self):
        """Create user with invalid payload returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_user_duplicate_email(self):
        """Create user with duplicate email returns 400."""
        first_response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        self.assertEqual(first_response.status_code, 201)

        second_response = self.client.post('/api/v1/users/', json={
            "first_name": "Janet",
            "last_name": "Doel",
            "email": "duplicate@example.com"
        })
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(second_response.get_json(), {"error": "Email already registered"})


class TestPlaceEndpoints(unittest.TestCase):
    """Tests for Place API endpoints."""

    def setUp(self):
        """Create app test client and isolate in-memory storages."""
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.amenity_repo._storage.clear()

        owner = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.place@example.com"
        })
        amenity = facade.create_amenity({"name": "WiFi"})

        self.owner_id = owner.id
        self.amenity_id = amenity.id

    def _valid_place_payload(self):
        """Return a valid place payload."""
        return {
            "title": "Cozy Studio",
            "description": "Nice place in city center",
            "price": 80,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        }

    def test_create_place(self):
        """Create place with valid payload returns 201."""
        response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Cozy Studio")
        self.assertEqual(data["owner_id"], self.owner_id)
        self.assertEqual(data["amenities"], [self.amenity_id])

    def test_create_place_invalid_data(self):
        """Create place with invalid payload returns 400."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -1,
            "latitude": 999,
            "longitude": 999,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_required_field(self):
        """Create place missing required field returns 400."""
        payload = self._valid_place_payload()
        payload.pop("owner_id")
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_owner_not_found(self):
        """Create place with unknown owner returns 400."""
        payload = self._valid_place_payload()
        payload["owner_id"] = "unknown-owner-id"
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_amenity_not_found(self):
        """Create place with unknown amenity returns 400."""
        payload = self._valid_place_payload()
        payload["amenities"] = ["unknown-amenity-id"]
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_out_of_range(self):
        """Create place with invalid latitude returns 400."""
        payload = self._valid_place_payload()
        payload["latitude"] = 90.1
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_out_of_range(self):
        """Create place with invalid longitude returns 400."""
        payload = self._valid_place_payload()
        payload["longitude"] = -180.1
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """List places returns 200 and contains created place."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertGreaterEqual(len(payload), 1)
        first_place = payload[0]
        self.assertIn("id", first_place)
        self.assertIn("title", first_place)
        self.assertIn("latitude", first_place)
        self.assertIn("longitude", first_place)

    def test_get_place_by_id(self):
        """Retrieve existing place by id returns 200."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], place_id)
        self.assertEqual(data["title"], "Cozy Studio")
        self.assertIn("owner", data)
        self.assertEqual(data["owner"]["id"], self.owner_id)
        self.assertEqual(data["owner"]["first_name"], "Jane")
        self.assertEqual(data["owner"]["last_name"], "Doe")
        self.assertEqual(data["owner"]["email"], "jane.place@example.com")
        self.assertIn("amenities", data)
        self.assertGreaterEqual(len(data["amenities"]), 1)
        self.assertEqual(data["amenities"][0]["id"], self.amenity_id)
        self.assertEqual(data["amenities"][0]["name"], "WiFi")

    def test_update_place_relationships_owner_and_amenities(self):
        """Update place owner and amenities, then verify related entities."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        new_owner = facade.create_user({
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith.place@example.com"
        })
        new_amenity = facade.create_amenity({"name": "Pool"})

        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "owner_id": new_owner.id,
            "amenities": [new_amenity.id]
        })
        self.assertEqual(update_response.status_code, 200)

        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        place_data = get_response.get_json()
        self.assertEqual(place_data["owner"]["id"], new_owner.id)
        self.assertEqual(place_data["owner"]["email"], "john.smith.place@example.com")
        self.assertEqual(len(place_data["amenities"]), 1)
        self.assertEqual(place_data["amenities"][0]["id"], new_amenity.id)
        self.assertEqual(place_data["amenities"][0]["name"], "Pool")

    def test_get_place_not_found(self):
        """Retrieve non-existent place returns 404."""
        response = self.client.get('/api/v1/places/not-found-id')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        """Update existing place returns 200."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated title",
            "price": 120
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Place updated successfully"})

        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        updated = get_response.get_json()
        self.assertEqual(updated["title"], "Updated title")
        self.assertEqual(updated["price"], 120.0)

    def test_create_place_boundary_coordinates_ok(self):
        """Create place with boundary coordinates returns 201."""
        payload = self._valid_place_payload()
        payload["latitude"] = -90
        payload["longitude"] = 180
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_reproduce_place_zero_values_no_500(self):
        """Reproduction case: zero values must not trigger 500."""
        payload = self._valid_place_payload()
        payload["price"] = 0
        payload["latitude"] = 0
        payload["longitude"] = 0

        response = self.client.post('/api/v1/places/', json=payload)
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(response.status_code, 201)

    def test_reproduce_place_update_zero_values_no_500(self):
        """Reproduction case on update: zero values must not trigger 500."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": 0,
            "latitude": 0,
            "longitude": 0
        })
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(response.status_code, 200)

    def test_update_place_invalid_data(self):
        """Update place with invalid values returns 400."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": -10,
            "latitude": 91,
            "longitude": -181
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_owner_not_found(self):
        """Update place with unknown owner returns 400."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "owner_id": "unknown-owner-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_amenity_not_found(self):
        """Update place with unknown amenity returns 400."""
        create_response = self.client.post('/api/v1/places/', json=self._valid_place_payload())
        self.assertEqual(create_response.status_code, 201)
        place_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "amenities": ["unknown-amenity-id"]
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_not_found(self):
        """Update non-existent place returns 404."""
        response = self.client.put('/api/v1/places/not-found-id', json={
            "title": "Updated title"
        })
        self.assertEqual(response.status_code, 404)


class TestReviewEndpoints(unittest.TestCase):
    """Tests for Review API endpoints."""

    def setUp(self):
        """Create app test client and seed required linked entities."""
        self.app = create_app()
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.review_repo._storage.clear()

        owner = facade.create_user({
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner.review@example.com"
        })
        reviewer = facade.create_user({
            "first_name": "Review",
            "last_name": "Writer",
            "email": "review.writer@example.com"
        })
        amenity = facade.create_amenity({"name": "WiFi"})

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "description": "Place used for review tests",
            "price": 99,
            "latitude": 48.0,
            "longitude": 2.0,
            "owner_id": owner.id,
            "amenities": [amenity.id]
        })

        self.assertEqual(place_response.status_code, 201)
        self.place_id = place_response.get_json()["id"]
        self.user_id = reviewer.id

    def _valid_review_payload(self):
        """Return a valid review payload."""
        return {
            "text": "Great place",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def _create_review(self):
        """Create a review and return its id."""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review_payload())
        self.assertEqual(response.status_code, 201)
        return response.get_json()["id"]

    def test_create_review(self):
        """Create review with valid payload returns 201."""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review_payload())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], "Great place")
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["user_id"], self.user_id)
        self.assertEqual(data["place_id"], self.place_id)

    def test_create_review_invalid_rating(self):
        """Create review with invalid rating returns 400."""
        payload = self._valid_review_payload()
        payload["rating"] = 0
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_review_missing_text(self):
        """Create review missing text returns 400."""
        payload = self._valid_review_payload()
        payload.pop("text")
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_review_empty_text(self):
        """Create review with blank text returns 400."""
        payload = self._valid_review_payload()
        payload["text"] = "   "
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_review_rating_not_integer(self):
        """Create review with non-integer rating returns 400."""
        payload = self._valid_review_payload()
        payload["rating"] = "5"
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_review_place_not_found(self):
        """Create review with unknown place returns 400."""
        payload = self._valid_review_payload()
        payload["place_id"] = "unknown-place-id"
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Place doesn't exists"})

    def test_create_review_user_not_found(self):
        """Create review with unknown user returns 400."""
        payload = self._valid_review_payload()
        payload["user_id"] = "unknown-user-id"
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "User doesn't exists"})

    def test_get_all_reviews(self):
        """List reviews returns 200 and lightweight payload."""
        review_id = self._create_review()
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        found = next((r for r in data if r["id"] == review_id), None)
        self.assertIsNotNone(found)
        self.assertIn("text", found)
        self.assertIn("rating", found)

    def test_get_review_by_id(self):
        """Retrieve existing review by id returns 200."""
        review_id = self._create_review()
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], review_id)
        self.assertEqual(data["user_id"], self.user_id)
        self.assertEqual(data["place_id"], self.place_id)

    def test_get_review_not_found(self):
        """Retrieve non-existent review returns 404."""
        response = self.client.get('/api/v1/reviews/not-found-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Review not found"})

    def test_get_reviews_by_place(self):
        """Place review list includes created review."""
        review_id = self._create_review()
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], review_id)
        self.assertEqual(data[0]["rating"], 5)

    def test_get_reviews_by_place_not_found(self):
        """Place review list for unknown place returns 404."""
        response = self.client.get('/api/v1/places/not-found-place-id/reviews')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Place not found"})

    def test_get_reviews_by_place_only_returns_related_reviews(self):
        """Each place reviews endpoint returns only its linked reviews."""
        first_review_id = self._create_review()

        second_place_response = self.client.post('/api/v1/places/', json={
            "title": "Second Review Place",
            "description": "Another place",
            "price": 120,
            "latitude": 49.0,
            "longitude": 3.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(second_place_response.status_code, 201)
        second_place_id = second_place_response.get_json()["id"]

        second_review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Review on second place",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": second_place_id
        })
        self.assertEqual(second_review_response.status_code, 400)
        self.assertEqual(second_review_response.get_json(), {"error": "Owner cannot review own place"})

        first_place_reviews = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(first_place_reviews.status_code, 200)
        first_ids = {r["id"] for r in first_place_reviews.get_json()}
        self.assertEqual(first_ids, {first_review_id})

        second_place_reviews = self.client.get(f'/api/v1/places/{second_place_id}/reviews')
        self.assertEqual(second_place_reviews.status_code, 200)
        second_ids = {r["id"] for r in second_place_reviews.get_json()}
        self.assertEqual(second_ids, set())

    def test_delete_review_keeps_other_place_reviews(self):
        """Deleting one review does not remove other linked reviews."""
        first_id = self._create_review()
        second_response = self.client.post('/api/v1/reviews/', json={
            "text": "Second review",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(second_response.get_json(), {"error": "Invalid input data"})

        delete_response = self.client.delete(f'/api/v1/reviews/{first_id}')
        self.assertEqual(delete_response.status_code, 200)

        place_reviews_response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(place_reviews_response.status_code, 200)
        remaining_ids = {r["id"] for r in place_reviews_response.get_json()}
        self.assertEqual(remaining_ids, set())

    def test_update_review(self):
        """Update existing review returns 200 and persists changes."""
        review_id = self._create_review()
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Review updated successfully"})

        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 200)
        updated = get_response.get_json()
        self.assertEqual(updated["text"], "Updated review")
        self.assertEqual(updated["rating"], 4)

    def test_update_review_not_found(self):
        """Update non-existent review returns 404."""
        response = self.client.put('/api/v1/reviews/not-found-id', json={
            "text": "Updated review",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Review not found"})

    def test_update_review_rating_zero_returns_400(self):
        """Updating rating to 0 returns 400 validation error."""
        review_id = self._create_review()
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Should fail",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_delete_review(self):
        """Delete existing review returns 200 then review is gone."""
        review_id = self._create_review()

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Review deleted successfully"})

        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

        place_reviews_response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(place_reviews_response.status_code, 200)
        self.assertEqual(place_reviews_response.get_json(), [])

    def test_delete_review_not_found(self):
        """Delete non-existent review returns 404."""
        response = self.client.delete('/api/v1/reviews/not-found-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Review not found"})


class TestAmenityEndpoints(unittest.TestCase):
    """Tests for Amenity API endpoints."""

    def setUp(self):
        """Create app test client and isolate in-memory amenity storage."""
        self.app = create_app()
        self.client = self.app.test_client()
        facade.amenity_repo._storage.clear()

    def test_create_amenity(self):
        """Create amenity with valid payload returns 201."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "  WiFi  "
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "WiFi")

    def test_create_amenity_invalid_empty_name(self):
        """Create amenity with empty name returns 400."""
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_amenity_invalid_blank_name(self):
        """Create amenity with blank name returns 400."""
        response = self.client.post('/api/v1/amenities/', json={"name": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_amenity_missing_name(self):
        """Create amenity without name returns 400."""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_create_amenity_name_too_long(self):
        """Create amenity with name > 50 chars returns 400."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "a" * 51
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_get_all_amenities(self):
        """List amenities returns 200 and created items."""
        first = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        second = self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        names = {a["name"] for a in data}
        self.assertEqual(names, {"WiFi", "Pool"})

    def test_get_amenity_by_id(self):
        """Retrieve existing amenity by id returns 200."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        self.assertEqual(create_response.status_code, 201)
        amenity_id = create_response.get_json()["id"]

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], amenity_id)
        self.assertEqual(data["name"], "Gym")

    def test_get_amenity_not_found(self):
        """Retrieve non-existent amenity returns 404."""
        response = self.client.get('/api/v1/amenities/not-found-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Amenity not found"})

    def test_update_amenity(self):
        """Update existing amenity returns 200 and persists name."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        self.assertEqual(create_response.status_code, 201)
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "  New Gym  "
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Amenity updated successfully"})

        get_response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json()["name"], "New Gym")

    def test_update_amenity_invalid_empty_name(self):
        """Update amenity with empty name returns 400."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_update_amenity_invalid_blank_name(self):
        """Update amenity with blank name returns 400 (no 500)."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_update_amenity_name_too_long(self):
        """Update amenity with name > 50 chars returns 400 (no 500)."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "b" * 51
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_update_amenity_missing_name(self):
        """Update amenity with missing name returns 400."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_update_amenity_unknown_field_only(self):
        """Update amenity with unknown field only returns 400."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_response.get_json()["id"]

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"foo": "bar"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid input data"})

    def test_update_amenity_not_found(self):
        """Update non-existent amenity returns 404."""
        response = self.client.put('/api/v1/amenities/not-found-id', json={"name": "Gym"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Amenity not found"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
