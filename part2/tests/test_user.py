#!/usr/bin/python3
"""Unit tests for User model."""

import unittest
import time
from datetime import datetime
import sys
import os

# ------------------------------------------------------------
# Import setup (avoid importing app/__init__.py which needs Flask)
# We add: part2/app/models to sys.path, then import user.py directly.
# ------------------------------------------------------------
TESTS_DIR = os.path.dirname(__file__)
PART2_DIR = os.path.abspath(os.path.join(TESTS_DIR, ".."))
MODELS_DIR = os.path.join(PART2_DIR, "app", "models")

if MODELS_DIR not in sys.path:
    sys.path.insert(0, MODELS_DIR)

from user import User  # noqa: E402


class TestUserCreate(unittest.TestCase):
    """Tests for User creation."""

    # ------------------------------------------------------------
    # Basic creation and BaseModel fields
    # ------------------------------------------------------------
    def test_create_valid_user(self):
        """Create user with valid fields."""
        u = User("John", "Doe", "john.doe@example.com")
        self.assertIsInstance(u.id, str)
        self.assertNotEqual(u.id.strip(), "")
        self.assertIsInstance(u.created_at, datetime)
        self.assertIsInstance(u.updated_at, datetime)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "john.doe@example.com")
        self.assertFalse(u.is_admin)

    def test_default_is_admin_false(self):
        """Default is_admin is False."""
        u = User("John", "Doe", "john.doe@example.com")
        self.assertFalse(u.is_admin)

    # ------------------------------------------------------------
    # first_name validation
    # ------------------------------------------------------------
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
        name = "a" * 51
        with self.assertRaises(ValueError):
            User(name, "Doe", "john.doe@example.com")

    # ------------------------------------------------------------
    # last_name validation
    # ------------------------------------------------------------
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
        name = "b" * 51
        with self.assertRaises(ValueError):
            User("John", name, "john.doe@example.com")

    # ------------------------------------------------------------
    # email validation
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # is_admin validation
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # update input validation
    # ------------------------------------------------------------
    def test_update_requires_dict(self):
        """Reject non-dict update payload."""
        with self.assertRaises(TypeError):
            self.u.update(["email", "x@y.com"])

    def test_update_empty_dict_no_change(self):
        """Empty update does not change updated_at."""
        old = self.u.updated_at
        self.u.update({})
        self.assertEqual(self.u.updated_at, old)

    # ------------------------------------------------------------
    # update first_name
    # ------------------------------------------------------------
    def test_update_first_name_ok(self):
        """Update first_name and update timestamp."""
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

    # ------------------------------------------------------------
    # update last_name
    # ------------------------------------------------------------
    def test_update_last_name_ok(self):
        """Update last_name and update timestamp."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({"last_name": "  Abbattista  "})
        self.assertEqual(self.u.last_name, "Abbattista")
        self.assertGreater(self.u.updated_at, old)

    def test_update_last_name_invalid(self):
        """Reject invalid last_name update."""
        old_name = self.u.last_name
        old_time = self.u.updated_at
        with self.assertRaises(ValueError):
            self.u.update({"last_name": ""})
        self.assertEqual(self.u.last_name, old_name)
        self.assertEqual(self.u.updated_at, old_time)

    # ------------------------------------------------------------
    # update email
    # ------------------------------------------------------------
    def test_update_email_ok_normalizes(self):
        """Update email with strip/lower."""
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

    # ------------------------------------------------------------
    # update is_admin
    # ------------------------------------------------------------
    def test_update_is_admin_ok(self):
        """Update is_admin."""
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

    # ------------------------------------------------------------
    # update unknown / protected fields
    # ------------------------------------------------------------
    def test_update_ignores_unknown_keys(self):
        """Unknown keys should not change timestamp."""
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

    def test_update_blocks_created_at_change(self):
        """Ignore attempts to change created_at."""
        old_created = self.u.created_at
        old_time = self.u.updated_at
        self.u.update({"created_at": datetime(2000, 1, 1)})
        self.assertEqual(self.u.created_at, old_created)
        self.assertEqual(self.u.updated_at, old_time)

    def test_update_multiple_fields_ok(self):
        """Update multiple fields at once."""
        old = self.u.updated_at
        time.sleep(0.01)
        self.u.update({
            "first_name": " Alice ",
            "last_name": " Smith ",
            "email": "ALICE.SMITH@EXAMPLE.COM",
            "is_admin": True,
        })
        self.assertEqual(self.u.first_name, "Alice")
        self.assertEqual(self.u.last_name, "Smith")
        self.assertEqual(self.u.email, "alice.smith@example.com")
        self.assertTrue(self.u.is_admin)
        self.assertGreater(self.u.updated_at, old)


if __name__ == "__main__":
    unittest.main(verbosity=2)