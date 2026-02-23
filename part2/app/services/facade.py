"""Facade layer for HBnB: orchestrates app logic and repositories."""

from app.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import AmenityModel


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
        self.amenity_repo = InMemoryRepository()

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

    def create_amenity(self, amenity_data):
        #Placeholder for logic to create an amenity
        amenity = AmenityModel(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        #placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, amenity_name):
        #Placeholder for logic to retrieve an amenity by name
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        #Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        #Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        amenity.save()
