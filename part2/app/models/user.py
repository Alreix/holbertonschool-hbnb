#!/usr/bin/python3
"""User model with basic validation."""

import re
from .base import BaseModel


class User(BaseModel):
    """Represent a user in the HBnB business layer."""

    # Simple email pattern for common cases
    EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Create a User instance with validated fields."""
        super().__init__()
        # Validate and normalize before storing
        self.first_name = self.validate_first_name(first_name)
        self.last_name = self.validate_last_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = self.validate_is_admin(is_admin)

    def validate_first_name(self, value):
        """Validate first_name rules."""
        if not isinstance(value, str):
            raise TypeError("first name must be a string")
        # Remove surrounding spaces
        value = value.strip()
        if not value:
            raise ValueError("first name is required")
        if len(value) > 50:
            raise ValueError("first name max length is 50")
        return value

    def validate_last_name(self, value):
        """Validate last_name rules."""
        if not isinstance(value, str):
            raise TypeError("last name must be a string")
        # Remove surrounding spaces
        value = value.strip()
        if not value:
            raise ValueError("last name is required")
        if len(value) > 50:
            raise ValueError("last name max length is 50")
        return value

    def validate_email(self, value):
        """Validate email format."""
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        # Remove spaces and standardize case
        value = value.strip().lower()
        if not value:
            raise ValueError("email is required")
        if " " in value:
            raise ValueError("email must not contain spaces")

        # Reject invalid email formats
        if re.fullmatch(self.EMAIL_PATTERN, value) is None:
            raise ValueError("email format must be like john.doe@example.com")
        return value

    def validate_is_admin(self, value):
        """Validate is_admin type."""
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    def update(self, data):
        """Update user fields with validation."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        # Only allow safe fields to be updated
        allowed = {"first_name", "last_name", "email", "is_admin"}
        changed = False

        for key, value in data.items():
            if key not in allowed:
                continue

            if key == "first_name":
                self.first_name = self.validate_first_name(value)
            elif key == "last_name":
                self.last_name = self.validate_last_name(value)
            elif key == "email":
                self.email = self.validate_email(value)
            elif key == "is_admin":
                self.is_admin = self.validate_is_admin(value)

            changed = True

        # Update timestamp only if something changed
        if changed:
            self.save()
