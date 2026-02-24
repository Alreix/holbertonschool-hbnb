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
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
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

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        amenity_ids = place_date.get("amenities", [])

        owner = self.user_repo.get(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in amity_ids:
            a = self.amenity_repo.get(amenity_id)
            if a is None:
                raise ValueError("Amenity not found")
            amenities.append(a)

        place = Place(
            title=place_data.get("title"),
            description=Place_data.get("description", ""),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner_id,
        )
        place.amenities = amenities

        self.place_repo.add(place)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": owner_id,
            "amenities": amenity_ids,
        }

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        owner = self.user_repo.get(place.owner if hasattr(place, "owner") else place.owner_id)
        owner_dict = None
        if owner:
            owner_dict = {
                "id": owner.id,
                "first_name": getattr(owner, "first_name", None),
                "last_name": getattr(owner, "last_name", None),
                "email": getattr(owner, "email", None),
            }
        
        amenities_list = []
        for a in getattr(place, "amenities", []):
            if hasattr(a, "id"):
                amenities_list.append({"id": a.id, "name": getattr(a, "name", None)})
            else:
                obj = self.amenity_repo.get(a)
                if obj:
                    amenities_list.append({"id": obj.id, "name": getattr(obj, "name", None)})

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_dict,
            "amenities": amenities_list,
        }

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in places:
        ]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place is None:
            return False

        if "amenities" in place_data:
            for amenity_id in place_data["amenities"]:
                if self.amenity_repo.get(amenity_id) is None:
                    raise ValueError("Amenity not found")

        place.update(place_data)
        return True
