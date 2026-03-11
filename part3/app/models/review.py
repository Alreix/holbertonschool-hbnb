"""Review model definitions.

This module provides the review entity and its validation helpers.
"""


from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """Represent a review written by a user for a place."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("reviews", lazy=True))
    place = db.relationship("Place", backref=db.backref("reviews", lazy=True))

    __table_args__ = (
        db.UniqueConstraint("user_id", "place_id", name="unique_user_place_review"),
    )

    def __init__(self, text, rating, place, user):
        """Initialize a review instance with validated fields."""
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    # Validation helpers
    def validate_text(self, value):
        """Validate the review text value."""
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        value = value.strip()
        if not value:
            raise ValueError("text cannot be empty")
        return value

    def validate_rating(self, value):
        """Validate the review rating value."""
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    def validate_place(self, value):
        """Validate the associated place instance."""
        if value is None:
            raise ValueError("place is required")
        if not isinstance(value, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(getattr(value, "id", None), str) or not value.id.strip():
            raise ValueError("place must be a valid id")
        return value

    def validate_user(self, value):
        """Validate the associated user instance."""
        if value is None:
            raise ValueError("user is required")
        if not isinstance(value, User):
            raise TypeError("user must be a User instance")
        if not isinstance(getattr(value, "id", None), str) or not value.id.strip():
            raise ValueError("user must have a valid id")
        return value

    # Update with validation
    def update(self, data):
        """Update review fields with validation.

        Args:
            data (dict): Fields to update.
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
