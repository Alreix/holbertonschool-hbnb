"""Review model with validation and relations."""

from .base import BaseModel
from .place import Place
from .user import User
import uuid


class Review(BaseModel):
    """
    Represent a review written by a user for a place.

    Attributes:
        id (str): UUID string (from BaseModel).
        text (str): Review text (required, non-empty).
        rating (int): Rating between 1 and 5.
        user_id (str): UUID string of the authoring user.
        place_id (str): UUID string of the reviewed place.
        created_at (datetime): Creation timestamp (from BaseModel).
        updated_at (datetime): Update timestamp (from BaseModel).
    """

    def __init__(self, text, rating, place, user):
        """Create a Review instance with validated fields."""
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = self.validate_place_id(place_id, "place_id")
        self.user_id = self.validate_user_id(user_id, "user_id")

    def validate_text(self, value):
        """Validate review text."""
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        value = value.strip()
        if not value:
            raise ValueError("text is required")
        return value

    def validate_rating(self, value):
        """Validate rating (must be int between 1 and 5)."""
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    def validate_uuid(self, value, field_name):
        """Validate UUID string."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} is required")
        try:
            uuid.UUID(value)
        except ValueError as exc:
            raise ValueError(f"{field_name} must be a valid UUID") from exc
        return value

    def update(self, data):
        """
        Update review fields with validation.

        Allowed fields:
            - text
            - rating
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        allowed = {"text", "rating"}
        changed = False

        for key, value in data.items():
            if key not in allowed:
                continue

            if key == "text":
                self.text = self.validate_text(value)
            elif key == "rating":
                self.rating = self.validate_rating(value)

            changed = True

        if changed:
            self.save()
