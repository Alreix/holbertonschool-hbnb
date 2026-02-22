"""Facade layer for HBnB: orchestrates app logic and repositories."""

from app.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    """
    Central service layer for HBnB operations.

    This class exposes high-level methods (create/get/update/list) and
    delegates persistence to repositories. It keeps API/controllers
    decoupled from storage details.
    """

    def __init__(self):
        """Initialize facade with required repositories."""
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a user from validated data and persist it."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Return a user by id, or None if not found."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Return a user by email, or None if not found."""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Return a list of all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user and return the updated user (or None)."""
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)
