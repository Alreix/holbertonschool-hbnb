# HBnB (Business Logic + REST API)

## Project Overview

This project provides the core backend foundation for HBnB:
- domain entities (`User`, `Place`, `Amenity`, `Review`)
- business rules and relationship validation
- REST API endpoints with consistent JSON responses
- modular architecture using the Facade pattern

Data persistence is currently in-memory through `InMemoryRepository`, which is fast for development and testing.

---

## Project Structure

```text
part2/
├── app/
│   ├── __init__.py
│   ├── api/v1/
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── amenities.py
│   │   └── reviews.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── amenity.py
│   │   └── review.py
│   ├── services/
│   │   └── facade.py
│   └── persistence/
│       └── repository.py
├── tests/
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Architecture

### Layers

1. **API Layer** (`app/api/v1/`)
	 - Defines routes with Flask-RESTX namespaces
	 - Validates input payload shape
	 - Returns HTTP status codes + JSON responses

2. **Business Logic Layer** (`app/models/` + `app/services/facade.py`)
	 - Implements entities and model-level validations
	 - Applies relationship and integrity rules
	 - Centralizes operations through `HBnBFacade`

3. **Persistence Layer** (`app/persistence/repository.py`)
	 - Stores entities in memory
	 - Provides `add/get/get_all/update/delete/get_by_attribute`

### Request Flow (Facade Pattern)

1. API endpoint receives request
2. Endpoint delegates operation to the facade
3. Facade coordinates models + repositories
4. Result is serialized and returned by API

---

## Business Logic: Entities and Responsibilities

### `BaseModel`
Shared fields and helpers:
- `id` (UUID string)
- `created_at`
- `updated_at`
- `save()` timestamp refresh
- `update(data)` controlled mutation

### `User`
- Identity and profile data (`first_name`, `last_name`, `email`, `is_admin`)
- Email normalization/validation
- Safe update behavior

### `Place`
- Property data (`title`, `description`, `price`, `latitude`, `longitude`, `owner`)
- Relations with amenities and reviews
- Validation for coordinates and pricing constraints

### `AmenityModel`
- Amenity definition (`name`)
- Validation and update support

### `Review`
- Review content (`text`, `rating`) and relations (`user`, `place`)
- Validation of rating range and relation integrity

---

## Facade Responsibilities (`HBnBFacade`)

The facade centralizes all domain operations:
- Users: create, read, list, update
- Amenities: create, read, list, update
- Places: create, read, list, update
- Reviews: create, read, list, update, delete, list by place

Key business constraints handled across the project:
- place owner must exist
- amenities linked to a place must exist
- review user and place must exist
- a user cannot review the same place twice
- owner cannot review their own place (enforced at API layer)

---

## API Endpoints Overview

### Users
- `POST /api/v1/users/` -> `201`, `400`
- `GET /api/v1/users/` -> `200`
- `GET /api/v1/users/<user_id>` -> `200`, `404`
- `PUT /api/v1/users/<user_id>` -> `200`, `404`, `400`

### Amenities
- `POST /api/v1/amenities/` -> `201`, `400`
- `GET /api/v1/amenities/` -> `200`
- `GET /api/v1/amenities/<amenity_id>` -> `200`, `404`
- `PUT /api/v1/amenities/<amenity_id>` -> `200`, `404`, `400`

### Places
- `POST /api/v1/places/` -> `201`, `400`
- `GET /api/v1/places/` -> `200`
- `GET /api/v1/places/<place_id>` -> `200`, `404`
- `PUT /api/v1/places/<place_id>` -> `200`, `404`, `400`

### Reviews
- `POST /api/v1/reviews/` -> `201`, `400`
- `GET /api/v1/reviews/` -> `200`
- `GET /api/v1/reviews/<review_id>` -> `200`, `404`
- `PUT /api/v1/reviews/<review_id>` -> `200`, `404`, `400`
- `DELETE /api/v1/reviews/<review_id>` -> `200`, `404`
- `GET /api/v1/places/<place_id>/reviews` -> `200`, `404`

---

## Validation Rules

- **User**
	- `first_name`, `last_name`, `email` are required
	- `email` must be valid
- **Place**
	- `title` is required
	- `price` must be non-negative
	- `latitude` must be between -90 and 90
	- `longitude` must be between -180 and 180
- **Review**
	- `text` is required
	- `rating` must be in `[1..5]`
	- `user_id` and `place_id` must reference existing entities
- **Amenity**
	- `name` is required

---

## Example Usage (Python)

```python
from app.services import facade

# Create user
owner = facade.create_user({
		"first_name": "Alice",
		"last_name": "Doe",
		"email": "alice@example.com"
})

# Create amenity
wifi = facade.create_amenity({"name": "WiFi"})

# Create place
place = facade.create_place({
		"title": "Cozy Apartment",
		"description": "A nice place to stay",
		"price": 100.0,
		"latitude": 37.7749,
		"longitude": -122.4194,
		"owner_id": owner.id,
		"amenities": [wifi.id]
})

# Read place
same_place = facade.get_place(place.id)

# Create review from another user
reviewer = facade.create_user({
		"first_name": "Bob",
		"last_name": "Smith",
		"email": "bob@example.com"
})

review = facade.create_review({
		"text": "Great place!",
		"rating": 5,
		"user_id": reviewer.id,
		"place_id": place.id
})
```

---

## Run the API

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Start server

```bash
python run.py
```

- Base URL: `http://127.0.0.1:5000`
- Swagger UI: `http://127.0.0.1:5000/api/v1/`

---

## cURL Test Examples

### Create a review

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
		"text": "Great great place to stay!",
		"rating": 5,
		"user_id": "272e94ac-2fd3-4393-8d1e-c3a4c7bd032e",
		"place_id": "73c39d1a-e913-42d1-8aa6-0c639c77f310"
}'
```

### Update user email (duplicate email -> 400)

```bash
curl -i -X PUT http://127.0.0.1:5000/api/v1/users/ced9f11b-5392-4b8d-a482-1c51513dcbfc \
-H "Content-Type: application/json" \
-d '{"first_name":"Alice","last_name":"Test","email":"alice_new@test.com"}'
```

Expected response:

```http
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.5 Python/3.12.3
Date: Thu, 26 Feb 2026 14:43:36 GMT
Content-Type: application/json
Content-Length: 44
Connection: close

{
		"error": "Email already registered"
}
```

### Create a place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
		"title": "Cozy Apartment",
		"description": "A nice place to stay",
		"price": 100.0,
		"latitude": 37.7749,
		"longitude": -122.4194,
		"owner_id": "32860df1-feb4-4ae6-8874-472b6d5150a5",
		"amenities": []
}'
```

Expected response:

```json
{
		"id": "73c39d1a-e913-42d1-8aa6-0c639c77f310",
		"title": "Cozy Apartment",
		"description": "A nice place to stay",
		"price": 100.0,
		"latitude": 37.7749,
		"longitude": -122.4194,
		"owner_id": "32860df1-feb4-4ae6-8874-472b6d5150a5",
		"amenities": []
}
```

### Get all reviews for one place

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/73c39d1a-e913-42d1-8aa6-0c639c77f310/reviews"
```

---

## Testing Strategy

Testing combines:
- manual tests with `curl` + Swagger
- automated tests with `unittest` (or `pytest`)

Recommended coverage:
- success paths for create/read/update/delete
- invalid payload formats
- required field checks
- boundary checks (`latitude`, `longitude`, `rating`)
- relationship checks (`owner_id`, `user_id`, `place_id`, amenities)
- not-found scenarios (`404`)

Suggested test log format:
- endpoint
- input payload
- expected output/status
- actual output/status
- notes/issues

---

## Notes

- IDs in curl examples are sample IDs and must exist in current in-memory data.
- Restarting the server resets all in-memory data.

## References

- Flask: https://flask.palletsprojects.com/
- Flask-RESTX: https://flask-restx.readthedocs.io/
- REST API practices: https://restfulapi.net/
- cURL: https://everything.curl.dev/
- Facade pattern: https://refactoring.guru/design-patterns/facade/python/example
# HBnB (Business Logic + REST API)

## Project Overview

This project implements the **Business Logic** and **REST API** layers of a simplified HBnB platform.

Main goals:
- Manage core entities: **User**, **Place**, **Amenity**, **Review**
- Validate business rules before persistence
- Expose clean HTTP endpoints for CRUD operations
- Keep architecture modular (API -> Facade -> Models/Repository)

Current storage is in-memory via `InMemoryRepository`, which makes local development and testing fast.

---

## Architecture

### Layers

1. **API Layer** (`app/api/v1/`)
   - Flask-RESTX namespaces and endpoints
   - Parses/validates input payload format
   - Calls the facade
   - Returns JSON responses and HTTP status codes

2. **Business Logic Layer** (`app/services/facade.py` + `app/models/`)
   - Encapsulates domain rules and consistency checks
   - Creates and updates entities
   - Enforces relationship constraints between entities

3. **Persistence Layer** (`app/persistence/repository.py`)
   - In-memory storage and retrieval by `id` or attribute

---

## Business Logic Layer: Entities and Responsibilities

### `BaseModel`
Common base class used by all entities:
- `id` (UUID string)
- `created_at`
- `updated_at`
- `save()` to refresh timestamps
- `update()` helper for mutations

### `User`
Represents an HBnB user.

Responsibilities:
- Validate `first_name`, `last_name`, `email`, `is_admin`
- Normalize email and protect data integrity
- Support controlled updates through `update(data)`

### `Place`
Represents a property listed in the platform.

Responsibilities:
- Validate `title`, `description`, `price`, `latitude`, `longitude`, `owner`
- Keep place relations (`amenities`, `reviews`)
- Support updates with validation

### `AmenityModel`
Represents a place amenity (e.g., WiFi, Pool).

Responsibilities:
- Validate amenity name
- Provide clean amenity records for place association

### `Review`
Represents a user review for a place.

Responsibilities:
- Validate `text`, `rating` (1-5), `place`, `user`
- Enforce valid references to existing `User` and `Place`

---

## Facade (`HBnBFacade`) Responsibilities

The facade is the main entry point for business operations. It centralizes:
- User operations: create, get, list, update
- Amenity operations: create, get, list, update
- Place operations: create, get, list, update
- Review operations: create, get, list, update, delete, list by place

It also enforces relationship/business rules such as:
- Place owner must exist
- Amenities linked to a place must exist
- A user cannot review the same place twice
- (API-level rule) A place owner cannot review their own place

---

## Example Usage (Python)

```python
from app.services import facade

# 1) Create a user
user = facade.create_user({
	"first_name": "Alice",
	"last_name": "Doe",
	"email": "alice@example.com"
})

# 2) Create an amenity
wifi = facade.create_amenity({"name": "WiFi"})

# 3) Create a place
place = facade.create_place({
	"title": "Cozy Apartment",
	"description": "A nice place to stay",
	"price": 100.0,
	"latitude": 37.7749,
	"longitude": -122.4194,
	"owner_id": user.id,
	"amenities": [wifi.id]
})

# 4) Read a place
same_place = facade.get_place(place.id)

# 5) Create a review
reviewer = facade.create_user({
	"first_name": "Bob",
	"last_name": "Smith",
	"email": "bob@example.com"
})

review = facade.create_review({
	"text": "Great place!",
	"rating": 5,
	"user_id": reviewer.id,
	"place_id": place.id
})
```

---

## API Run Instructions

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Start server

```bash
python run.py
```

Server default URL:
- `http://127.0.0.1:5000`

Swagger/OpenAPI docs:
- `http://127.0.0.1:5000/api/v1/`

---

## cURL Test Examples

### Create a review

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
	"text": "Great great place to stay!",
	"rating": 5,
	"user_id": "272e94ac-2fd3-4393-8d1e-c3a4c7bd032e",
	"place_id": "73c39d1a-e913-42d1-8aa6-0c639c77f310"
}'
```

### Update user email (duplicate email -> 400)

```bash
curl -i -X PUT http://127.0.0.1:5000/api/v1/users/ced9f11b-5392-4b8d-a482-1c51513dcbfc \
-H "Content-Type: application/json" \
-d '{"first_name":"Alice","last_name":"Test","email":"alice_new@test.com"}'
```

Example response:

```http
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.5 Python/3.12.3
Date: Thu, 26 Feb 2026 14:43:36 GMT
Content-Type: application/json
Content-Length: 44
Connection: close

{
	"error": "Email already registered"
}
```

### Create a place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
	"title": "Cozy Apartment",
	"description": "A nice place to stay",
	"price": 100.0,
	"latitude": 37.7749,
	"longitude": -122.4194,
	"owner_id": "32860df1-feb4-4ae6-8874-472b6d5150a5",
	"amenities": []
}'
```

Example response:

```json
{
	"id": "73c39d1a-e913-42d1-8aa6-0c639c77f310",
	"title": "Cozy Apartment",
	"description": "A nice place to stay",
	"price": 100.0,
	"latitude": 37.7749,
	"longitude": -122.4194,
	"owner_id": "32860df1-feb4-4ae6-8874-472b6d5150a5",
	"amenities": []
}
```

---

## Notes

- IDs used in curl examples are sample values and must exist in your current in-memory data.
- Since persistence is in-memory, restarting the server resets all data.

