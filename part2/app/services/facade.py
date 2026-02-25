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

    def create_amenity(self, amenity_data):
        """Create a new amenity and return it."""
        amenity = AmenityModel(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, amenity_name):
        """Retrieve an amenity by its name."""
        return self.amenity_repo.get_by_attribute("name", amenity_name)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity and return the updated object (or None)."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        amenity.save()
        return amenity

     def create_place(self, place_data):
        """
        Create a Place with:
          - validation handled by Place model (price/lat/lon/title/owner)
          - owner_id must exist
          - amenities ids must exist
        Returns: dict (as in the task examples)
        """
        if not isinstance(place_data, dict):
            raise TypeError("place_data must be a dict")

        required = ["title", "price", "latitude", "longitude", "owner_id", "amenities"]
        for k in required:
            if k not in place_data:
                raise ValueError(f"{k} is required")

        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities", [])
        if not isinstance(amenity_ids, list):
            raise TypeError("amenities must be a list of amenity IDs")

        amenities = []
        for aid in amenity_ids:
            a = self.amenity_repo.get(aid)
            if a is None:
                raise ValueError("Amenity not found")
            amenities.append(a)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner_id,
        )

        place.amenities = amenities
        place.reviews = []

        self.place_repo.add(place)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": owner_id,
            "amenities": [a.id for a in amenities],
        }

    def get_place(self, place_id):
        """
        Return place details (dict) including:
          - owner (nested user dict)
          - amenities (list of nested dicts)
        """
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        owner_id = place.owner.id if hasattr(place.owner, "id") else place.owner
        owner = self.user_repo.get(owner_id)

        owner_dict = None
        if owner:
            owner_dict = {
                "id": owner.id,
                "first_name": getattr(owner, "first_name", None),
                "last_name": getattr(owner, "last_name", None),
                "email": getattr(owner, "email", None),
            }

        amenities_list = []
        for a in (place.amenities or []):
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
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_dict,
            "amenities": amenities_list,
        }

    def get_all_places(self):
        """Return list of all places (light format)."""
        places = self.place_repo.get_all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in places
        ]

    def update_place(self, place_id, place_data):
        """
        Update allowed fields. Must validate:
          - price >= 0
          - latitude range
          - longitude range
          - owner if provided must exist
          - amenities if provided must exist
        Returns: True if updated, False if not found
        """
        place = self.place_repo.get(place_id)
        if place is None:
            return False

        if not isinstance(place_data, dict):
            raise TypeError("place_data must be a dict")

        if "owner_id" in place_data:
            new_owner = self.user_repo.get(place_data["owner_id"])
            if new_owner is None:
                raise ValueError("Owner not found")
            place_data = dict(place_data)
            place_data["owner"] = place_data.pop("owner_id")

        if "amenities" in place_data:
            amenity_ids = place_data["amenities"]
            if not isinstance(amenity_ids, list):
                raise TypeError("amenities must be a list of amenity IDs")

            new_amenities = []
            for aid in amenity_ids:
                a = self.amenity_repo.get(aid)
                if a is None:
                    raise ValueError("Amenity not found")
                new_amenities.append(a)
            place.amenities = new_amenities

        allowed_for_place = {k: v for k, v in place_data.items()
                             if k in {"title", "description", "price", "latitude", "longitude", "owner"}}
        if allowed_for_place:
            place.update(allowed_for_place)
            place.save()

        return True

    def create_review(self, review_data):
        """
        Must create Review with Review model which requires Place and User instances.
        Returns: Review object (your API expects .id, .user.id, .place.id)
        """
        if not isinstance(review_data, dict):
            raise TypeError("review_data must be a dict")

        for k in ("text", "rating", "user_id", "place_id"):
            if k not in review_data:
                raise ValueError(f"{k} is required")

        user = self.user_repo.get(review_data["user_id"])
        if user is None:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data["place_id"])
        if place is None:
            raise ValueError("Place not found")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place=place,
            user=user,
        )
        self.review_repo.add(review)

        if place.reviews is None:
            place.reviews = []
        place.reviews.append(review.id)
        place.save()

        return review

    def get_review(self, review_id):
        """Return Review object or None."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return list of Review objects."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Return list of Review objects (or dicts) for a place.
        Consigne expects list like: [{id,text,rating},...]
        For the /places/<id>/reviews endpoint, easiest is to return list of dicts.
        """
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        review_ids = getattr(place, "reviews", []) or []
        out = []
        for rid in review_ids:
            r = self.review_repo.get(rid)
            if r:
                out.append({"id": r.id, "text": r.text, "rating": r.rating})
        return out

    def update_review(self, review_id, review_data):
        """Return True if updated, False if not found."""
        review = self.review_repo.get(review_id)
        if review is None:
            return False
        review.update(review_data)
        return True

    def delete_review(self, review_id):
        """Return True if deleted, False if not found."""
        review = self.review_repo.get(review_id)
        if review is None:
            return False

        place = review.place
        if place and getattr(place, "reviews", None):
            if review_id in place.reviews:
                place.reviews.remove(review_id)
                place.save()

        self.review_repo.delete(review_id)
        return True
