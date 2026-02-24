from app.services import facade
from flask_restx import Namespace, Resource, fields

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the amenity response model
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(required=True, description='Unique ID of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity created')
    @api.response(400, 'Invalid input')
    @api.response(500, 'Server error')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        try:
            if not amenity_data or 'name' not in amenity_data:
                return {'error': 'Name is required'}, 400

            name = amenity_data['name']
            if not isinstance(name, str):
                return {'error': 'Name must be a string'}, 400
            name = name.strip()
            if not name:
                return {'error': 'Name cannot be empty'}, 400

            if facade.get_amenity_by_name(name):
                return {'error': 'Amenity already exists'}, 400

            new_amenity = facade.create_amenity({'name': name})
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.response(200, 'List retrieved')
    @api.response(500, 'Server error')
    def get(self):
        """List all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [{'id': a.id, 'name': a.name} for a in amenities], 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity retrieved')
    @api.response(404, 'Not found')
    @api.response(500, 'Server error')
    def get(self, amenity_id):
        """Get amenity by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return {'id': amenity.id, 'name': amenity.name}, 200
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Not found')
    @api.response(500, 'Server error')
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            existing = facade.get_amenity(amenity_id)
            if not existing:
                return {'error': 'Amenity not found'}, 404

            amenity_data = api.payload
            if not amenity_data or 'name' not in amenity_data:
                return {'error': 'Name is required'}, 400

            name = amenity_data['name'].strip()
            if not name:
                return {'error': 'Name cannot be empty'}, 400

            updated = facade.update_amenity(amenity_id, {'name': name})
            return {'id': updated.id, 'name': updated.name}, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error', 'message': str(e)}, 500
