from .base import BaseModel


class AmenityModel(BaseModel):
    """Represents an amenity that can be assigned to a place."""

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        """Validate amenity name"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name must be a non-empty string")

        name = name.strip()

        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters")

        return name

    def update(self, data):
        """Update amenity attributes"""
        if 'name' in data:
            self.name = self.validate_name(data['name'])

        # Update timestamp
        super().save()

    def save(self):
        """Save the amenity (update timestamp)"""
        super().save()
