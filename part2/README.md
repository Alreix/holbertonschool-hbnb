# HBnB - Part 2: Business Logic and REST API

## Introduction

This stage of the HBnB project corresponds to the application implementation phase, based on the architecture defined previously.
The goal is to build a functional and scalable foundation with Python, Flask, and Flask-RESTX by setting up:

- the Presentation layer (REST API)
- the Business Logic layer (services + models)
- the Persistence layer (in-memory repository)

The application applies layered software architecture principles, along with the **Facade** and **Repository** patterns, to improve maintainability, readability, and scalability.

Note: JWT authentication and role management are not covered in this stage. They are planned for the next stage.

---

## Project Objectives

- Build a modular API with Flask and Flask-RESTX.
- Implement business logic for `User`, `Place`, `Amenity`, and `Review` entities.
- Set up in-memory persistence via `InMemoryRepository`.
- Document API endpoints (Swagger UI).
- Test and validate endpoints with `unittest` and `cURL`.

---

## Project Architecture (Schema)

```text
Client (cURL / Postman / Frontend)
            |
            v
+----------------------------------+
| Presentation Layer (app/api/v1/) |
| Flask-RESTX Namespaces/Routes    |
+----------------------------------+
            |
            v
+----------------------------------+
| Business Layer (app/services/)   |
| HBnBFacade                       |
+----------------------------------+
            |
            v
+----------------------------------+
| Domain Models (app/models/)      |
| User / Place / Amenity / Review  |
+----------------------------------+
            |
            v
+----------------------------------+
| Persistence (app/persistence/)   |
| InMemoryRepository               |
+----------------------------------+
```

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
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── tests/
│   └── test_classes.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Layer Details

### 1) Presentation Layer (API)

Files: `app/api/v1/*.py`

Responsibilities:
- define REST endpoints (`GET`, `POST`, `PUT`, `DELETE`)
- validate input payloads
- return consistent JSON responses
- expose Swagger documentation through Flask-RESTX

Documentation URL:
- `http://127.0.0.1:5000/api/v1/`

### 2) Business Layer (Services / Facade)

File: `app/services/facade.py`

Responsibilities:
- centralize business logic in `HBnBFacade`
- orchestrate CRUD operations across all entities
- validate relationships between entities (owner, user, place, amenities)

### 3) Persistence Layer (Repository)

File: `app/persistence/repository.py`

Responsibilities:
- store objects in memory
- provide shared operations: `add`, `get`, `get_all`, `update`, `delete`, `get_by_attribute`

### 4) Domain Models

Files: `app/models/*.py`

Main entities:
- `BaseModel`
- `User`
- `Place`
- `AmenityModel`
- `Review`

### 5) Configuration and Runtime

- `config.py`: global application configuration
- `run.py`: server entry point
- `app/__init__.py`: Flask factory + API namespace registration

---

## Main Features

### Users
- user creation
- list/detail retrieval
- profile update
- email uniqueness check

### Places
- place creation with an existing owner
- amenities list assignment by IDs
- list/detail retrieval
- attribute and relationship updates
- reviews endpoint for a place

### Amenities
- amenity creation
- list/detail retrieval
- amenity update

### Reviews
- review creation linked to existing user/place
- list/detail retrieval
- review update
- review deletion
- business constraints applied (data validation, relationship rules)

---

## API Routes

Base URL: `http://127.0.0.1:5000`

### Users
- `POST /api/v1/users/`
- `GET /api/v1/users/`
- `GET /api/v1/users/<user_id>`
- `PUT /api/v1/users/<user_id>`

### Amenities
- `POST /api/v1/amenities/`
- `GET /api/v1/amenities/`
- `GET /api/v1/amenities/<amenity_id>`
- `PUT /api/v1/amenities/<amenity_id>`

### Places
- `POST /api/v1/places/`
- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`
- `PUT /api/v1/places/<place_id>`
- `GET /api/v1/places/<place_id>/reviews`

### Reviews
- `POST /api/v1/reviews/`
- `GET /api/v1/reviews/`
- `GET /api/v1/reviews/<review_id>`
- `PUT /api/v1/reviews/<review_id>`
- `DELETE /api/v1/reviews/<review_id>`

---

## Run Locally

### 1) Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 2) Start server

```bash
python3 run.py
```

---

## cURL Examples (Terminal Only)

### Create a user

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'
```

### Create an amenity

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": "WiFi"
}'
```

### Create a place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Cozy Studio",
    "description": "Near center",
    "price": 80,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "<OWNER_ID>",
    "amenities": ["<AMENITY_ID>"]
}'
```

### Create a review

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Great stay",
    "rating": 5,
    "user_id": "<REVIEWER_ID>",
    "place_id": "<PLACE_ID>"
}'
```

### Get reviews by place

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews"
```

---

## Test Endpoints

Comprehensive tests have been performed on all API endpoints using `cURL` to validate the application's behavior in various scenarios (creation, retrieval, update, deletion, error handling).

The detailed report of endpoint tests and unittest documentation is available in the attached documentation: [Endpoint Test Documentation](tests/endpoint_test_documentation.md)

---

## Tests and Validation

### Automated tests

```bash
python3 -m unittest tests/test_classes.py -v
```

### Manual tests

- Swagger UI (`/api/v1/`)
- `cURL` commands (examples above)

Validated points:
- happy-path scenarios
- payload validation
- `400/404` errors
- entity relationships
- response serialization regression checks

---

## Development Workflow

Workflow used:
- layer-by-layer implementation (models -> facade -> API)
- incremental validation with `unittest`
- manual verification with `cURL`
- continuous documentation updates (`README`)

---

## Authors

- HBnB Project Team
- Contributors: Faroux Joan, Abbattista Morgane, Uzun Bengin

---

## Notes

- In-memory persistence only.
- Restarting the server resets data.
- Current minimal dependencies: `flask`, `flask-restx`.
