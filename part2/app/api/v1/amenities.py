from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """Handle creation and listing of amenities."""

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity."""
        data = api.payload

        if not data or "name" not in data:
            return {"error": "Invalid input data"}, 400

        amenity = facade.create_amenity(data)
        return amenity, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Return all amenities."""
        amenities = facade.get_all_amenities()
        return amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Handle operations on a single amenity."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by its ID."""
        amenity = facade.get_amenity_by_id(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity by ID."""
        data = api.payload

        if not data or "name" not in data:
            return {"error": "Invalid input data"}, 400

        updated = facade.update_amenity(amenity_id, data)

        if not updated:
            return {"error": "Amenity not found"}, 404

        return updated, 200
