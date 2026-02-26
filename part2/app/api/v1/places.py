"""Place API endpoints.

This module defines REST resources used to create, list, retrieve, and update
places, as well as retrieve reviews for a specific place.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Resource for place collection operations."""
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place.

        Returns:
            tuple[dict, int]: Created place payload and HTTP 201 status.
        """
        data_place = api.payload

        try:
            new_place = facade.create_place(data_place)

        except (TypeError, ValueError):
            return {"error": "Invalid input data"}, 400
        
        return {
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner,
            'amenities': new_place.amenities,
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places.

        Returns:
            tuple[list[dict], int]: List of places and HTTP 200 status.
        """
        all_places = facade.get_all_places()
        return [
            {
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'owner_id': p.owner,
            'amenities': p.amenities,
            }
            for p in all_places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource for single-place operations."""
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve place details by ID.

        Args:
            place_id (str): Identifier of the place.

        Returns:
            tuple[dict, int]: Place details and HTTP 200 status.
            tuple[dict, int]: Error payload and HTTP 404 status if not found.
        """
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return [
            {
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner,
            'amenities': place.amenities,
            }
        ], 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place by ID.

        Args:
            place_id (str): Identifier of the place to update.

        Returns:
            tuple[dict, int]: Success payload and HTTP 200 status.
            tuple[dict, int]: Error payload and HTTP 404/400 status.
        """
        try:
            ok = facade.update_place(place_id, api.payload)
            if not ok:
                return {"error": "Place not found"}, 404
            return {"message": "Place updated successfully"}, 200
        except (TypeError, ValueError):
            return {"error": "Invalid input data"}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Resource for place review listing."""
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a place.

        Args:
            place_id (str): Identifier of the place.

        Returns:
            tuple[list[dict], int]: List of reviews and HTTP 200 status.
            tuple[dict, int]: Error payload and HTTP 404 status if place is missing.
        """
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [
            {
            "id": reviews.id,
            "text": reviews.text,
            "rating": reviews.rating,
            "user_id": reviews.user.id,
            "place_id": reviews.place.id
            }
        ], 200
