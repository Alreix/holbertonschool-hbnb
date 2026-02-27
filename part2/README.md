# HBnB - Part 2 (Business Logic + REST API)

## Overview

This repository contains Part 2 of the HBnB backend project:

- domain models (`User`, `Place`, `AmenityModel`, `Review`)
- service layer with a Facade (`HBnBFacade`)
- in-memory persistence (`InMemoryRepository`)
- REST API with Flask-RESTX namespaces
- unit and endpoint tests in `tests/test_classes.py`

Persistence is currently in-memory only: restarting the app clears all data.

---

## Tech Stack

- Python 3
- Flask
- Flask-RESTX
- `unittest` for tests

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

## Architecture

### 1) API Layer (`app/api/v1/`)

- Defines routes with Flask-RESTX namespaces.
- Validates request payload shape.
- Returns JSON responses with explicit status codes.

### 2) Service Layer (`app/services/facade.py`)

- Centralizes domain operations:
  - users: create/get/list/update
  - amenities: create/get/list/update
  - places: create/get/list/update
  - reviews: create/get/list/update/delete + list by place
- Enforces cross-entity consistency:
  - place owner must exist
  - amenities linked to a place must exist
  - review user and place must exist
  - one review per user per place

### 3) Domain Models (`app/models/`)

- `BaseModel`: `id`, `created_at`, `updated_at`, `save()`, `update()`
- `User`: name/email validation + optional `is_admin`
- `Place`: title/price/coordinates/owner validation + relations
- `AmenityModel`: amenity name validation
- `Review`: text/rating validation + strict `User`/`Place` relations

### 4) Persistence Layer (`app/persistence/repository.py`)

- Generic repository interface.
- In-memory implementation with:
  - `add`, `get`, `get_all`, `update`, `delete`, `get_by_attribute`

---

## API Routes

Base URL: `http://127.0.0.1:5000`

Swagger UI: `http://127.0.0.1:5000/api/v1/`

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

## Validation Rules (Implemented)

### User

- `first_name`: required, string, max 50
- `last_name`: required, string, max 50
- `email`: required, valid format, trimmed + lowercased
- `is_admin`: boolean

### Place

- `title`: required, string, max 100
- `description`: optional, max 1000
- `price`: numeric, `>= 0`
- `latitude`: numeric, between `-90` and `90`
- `longitude`: numeric, between `-180` and `180`
- `owner_id`: must reference an existing user
- `amenities`: list of existing amenity IDs

### Amenity

- `name`: required, non-empty string, max 50

### Review

- `text`: required, non-empty string
- `rating`: integer between `1` and `5`
- `user_id`: must reference an existing user
- `place_id`: must reference an existing place
- owner cannot review their own place (API-level check)

---

## Run Locally

### 1) Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 2) Start the server

```bash
python3 run.py
```

---

## cURL Examples (Terminal Only)

Use these directly in a terminal while the API is running.

### 1) Create a user

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com"
}'
```

### 2) Create an amenity

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi"
}'
```

### 3) Create a place

Replace `<OWNER_ID>` and `<AMENITY_ID>` with real IDs from previous responses.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Studio",
    "description": "Near center",
    "price": 80,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "<OWNER_ID>",
    "amenities": ["<AMENITY_ID>"]
}'
```

### 4) Create a second user (reviewer)

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john@example.com"
}'
```

### 5) Create a review

Replace `<REVIEWER_ID>` and `<PLACE_ID>`.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great stay",
    "rating": 5,
    "user_id": "<REVIEWER_ID>",
    "place_id": "<PLACE_ID>"
}'
```

### 6) Get reviews for one place

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews"
```

### 7) Update a review

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated comment",
    "rating": 4,
    "user_id": "<REVIEWER_ID>",
    "place_id": "<PLACE_ID>"
}'
```

### 8) Error example: owner cannot review own place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Self review",
    "rating": 5,
    "user_id": "<OWNER_ID>",
    "place_id": "<PLACE_ID>"
}'
```

Expected error:

```json
{"error":"Owner cannot review own place"}
```

### 9) Error example: duplicate review from same user on same place

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Second review attempt",
    "rating": 4,
    "user_id": "<REVIEWER_ID>",
    "place_id": "<PLACE_ID>"
}'
```

Expected error:

```json
{"error":"Invalid input data"}
```

---

## Run Tests

```bash
python3 -m unittest tests/test_classes.py -v
```

Test suite covers:

- model validation and update behavior
- repository/facade-integrated endpoint behavior
- success and error paths for all exposed API resources

---

## Notes

- Data is stored in memory only.
- Restarting the app resets users, places, amenities, and reviews.
- `requirements.txt` currently contains minimal direct dependencies (`flask`, `flask-restx`).
