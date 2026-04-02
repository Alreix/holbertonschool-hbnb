# HBnB - Holberton Project

## Project Description

HBnB is a progressive accommodation platform built from a learning roadmap at Holberton School. It progresses through planning, service implementation, database support, and a browser UI integration.

## Objectives

- Provide a modular design based on separated responsibilities.
- Build RESTful operations for core resources: user, place, amenity, review.
- Implement a business layer controller and decoupled persistence.
- Add secure access with JSON Web Tokens and password hashing.
- Link frontend interactions to the API for a complete user flow.

## Architecture

- Layers and roles:
- Presentation layer: HTTP API endpoints in the app packages.
- Business layer: service and facade components for domain rules.
- Persistence layer: in-memory for early phases, SQLAlchemy for production.
- Database engine: SQLite with model relationships.

## Project Structure

```text
holbertonschool-hbnb/
├── part1/                                    # Phase 1 - Design
│   └── TECHNICAL_DOCUMENTATION.md            # Technical documentation with UML diagrams
├── part2/                                    # Phase 2 - Implementation with in-memory storage
│   ├── app/                                  # Application package
│   │   ├── api/v1/                           # REST API endpoints
│   │   ├── models/                           # Data models
│   │   ├── services/                         # Business logic (Facade)
│   │   └── persistence/                      # In-memory persistence layer
│   ├── tests/                                # Test suite
│   ├── config.py                             # Application configuration
│   ├── run.py                                # Application entry point
│   ├── requirements.txt                      # Python dependencies
│   └── README.md                             # Part 2 documentation
├── part3/                                    # Phase 3 - Database and Authentication
│   ├── app/                                  # Application package
│   │   ├── api/v1/                           # REST API endpoints with auth
│   │   ├── models/                           # SQLAlchemy models
│   │   ├── services/                         # Business logic (Facade)
│   │   └── persistence/                      # SQLAlchemy repository
│   ├── instance/sql/                         # SQL schema files
│   ├── tests/                                # Test suite
│   ├── config.py                             # Application configuration
│   ├── run.py                                # Application entry point
│   ├── requirements.txt                      # Python dependencies
│   └── README.md                             # Part 3 documentation
└── part4/                                    # Phase 4 - Frontend Integration
    ├── add_review.html                       # Review submission page
    ├── index.html                            # Home page with places list
    ├── login.html                            # Login page
    ├── place.html                            # Place details page
    ├── scripts.js                            # Main JavaScript with API calls
    ├── styles.css                            # Application styles
    ├── images/                               # Images (logo, favicon)
    └── README.md                             # Part 4 documentation
```

## Implemented Features

### User Management

- User registration handles field validation and uniqueness.
- Passwords are hashed with bcrypt before storing.
- Login issues a JWT token for secured endpoint access.

### Place Management

- Place operations include creation, listing, update, and deletion.
- Ownership verification and location bounds are applied.
- Amenity attachments can be managed on places.

### Amenity Management

- Amenity CRUD paths are available and protected.
- Name constraints prevent duplicates and invalid entries.

### Review Management

- Users can create reviews associated with a place.
- Ratings and text are validated with clear boundaries.
- Review editing/removal is limited to owner/admin roles.

### Security

- API endpoints use JWT validation for protected routes.
- Admin status and ownership are checked before updates/deletes.

### Persistence

- Part2 relies on in-memory repository for fast iteration.
- Part3 and Part4 use SQLAlchemy with SQLite persistence.

## Development Status

### Part 1 - Design and Modeling (Completed)
- Designed architecture and workflows by mapping use cases.
- Documented entity relationships and process flows.
- Defined interfaces for facade and repository roles.

### Part 2 - Implementation with In-Memory Storage (Completed)
- Implemented models, service facade, and in-memory repository.
- Added API routes with validation and error handling.
- Includes automated tests for API and business rules.

### Part 3 - Database and Authentication (Completed)
- Implemented SQLAlchemy models and database persistence.
- Added JWT authentication and protected routes.
- Developed role-based access checks and repository patterns.

### Part 4 - Frontend Integration (Completed)
- Implemented static UI pages (index, login, place, add_review).
- Connected frontend to backend API using JS fetch calls.
- Added CORS support and client-side interactions.

## Running Part4 (Frontend + Backend)

1. Start backend from `part3`:

```bash
cd part3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 init_db.py
python3 run.py
```

2. Start frontend from `part4`:

```bash
cd part4
python3 -m http.server 8000
```

3. Open `http://localhost:8000`.

## Notes

- API path is `/api/v1`.
- Part3/Part4 backend provides CORS for local frontend connections.
- The data model covers users, places, amenities, reviews, and place-amenity relations.

## Technologies

### Backend
- Python 3.x with Flask and organized namespaces.
- REST API through Flask-RESTX and JWT authentication.
- Password security managed with Flask-Bcrypt.
- CORS support through Flask-CORS.
- Database ORM via SQLAlchemy + Flask-SQLAlchemy.

### Frontend
- HTML5 templates and CSS3 styling.
- Client-side interactions powered by JavaScript (ES6+).
- Fetch-based calls to the backend API.

### Database
- SQLite for local development and test runs.

### Architecture Patterns
- Facade pattern for service orchestration.
- Repository abstraction for data access.
- Layered separation for maintainability.

### Documentation
- Markdown and clear inline structure for each part.

### Testing
- `unittest` for unit/integration coverage.

## API Endpoints

### Authentication (Part 3)
- POST /api/v1/auth/login : Authenticates user credentials and returns JWT.
- GET /api/v1/auth/protected : Endpoint requiring a valid JWT.

### Users
- POST /api/v1/users/ : Register a new user.
- GET /api/v1/users/ : List users (admin-level fields protected).
- GET /api/v1/users/<user_id> : Get details for a user.
- PUT /api/v1/users/<user_id> : Update user profile (owner/admin).

### Places
- POST /api/v1/places/ : Create a new place entry.
- GET /api/v1/places/ : Retrieve all places.
- GET /api/v1/places/<place_id> : Retrieve a place.
- PUT /api/v1/places/<place_id> : Modify a place (owner/admin).
- GET /api/v1/places/<place_id>/reviews : Get place's reviews.

### Reviews
- POST /api/v1/reviews/ : Create a new review.
- GET /api/v1/reviews/ : Get all reviews.
- GET /api/v1/reviews/<review_id> : View one review.
- PUT /api/v1/reviews/<review_id> : Edit review (author/admin).
- DELETE /api/v1/reviews/<review_id> : Delete review (author/admin).

### Amenities
- POST /api/v1/amenities/ : Create a new amenity.
- GET /api/v1/amenities/ : List amenities.
- GET /api/v1/amenities/<amenity_id> : Get amenity details.
- PUT /api/v1/amenities/<amenity_id> : Update amenity.

### Common HTTP Status Codes
- 200 OK : Request succeeded.
- 201 Created : Resource created.
- 400 Bad Request : Input validation or format error.
- 401 Unauthorized : Missing/invalid token.
- 403 Forbidden : Access right denied.
- 404 Not Found : Resource missing.

## Authors

- Abbattista Morgane
- Faroux Joan
- Uzun Bengin

## License

Project produced for academic evaluation at Holberton School.
