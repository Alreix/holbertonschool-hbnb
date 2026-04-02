# HBnB - Holberton Project

## Project Description

HBnB is an accommodation rental application developed as part of the Holberton School curriculum. This project implements a complete web application with REST API, business logic layer, and database persistence.

## Objectives

Development of a complete web application following best practices:

- Layered Architecture: Separation between presentation, business logic, and data persistence
- REST API: RESTful interface with Flask-RESTX
- UML Modeling: Technical documentation with UML diagrams
- Design Patterns: Repository and Facade patterns
- Authentication: JWT-based authentication with password hashing
- Database: SQLAlchemy ORM with SQLite

## Architecture

Layered architecture implementation:

- HBnB Application
  - Presentation Layer (REST API with Flask-RESTX)
  - Business Logic Layer (Models and Facade)
  - Persistence Layer (Repository Pattern)
  - Database Layer (SQLAlchemy with SQLite)

## Project Structure

- holbertonschool-hbnb/
  - part1/ (Phase 1 - Design and modeling)
    - TECHNICAL_DOCUMENTATION.md (Technical documentation with UML diagrams)
  - part2/ (Phase 2 - Implementation with in-memory storage)
    - app/
      - api/v1/ (REST API endpoints)
      - models/ (Data models)
      - services/ (Business logic - Facade)
      - persistence/ (In-memory persistence layer)
    - tests/ (Test suite)
    - config.py (Application configuration)
    - run.py (Application entry point)
    - requirements.txt (Python dependencies)
    - README.md (Part 2 documentation)
  - part3/ (Phase 3 - Database and Authentication)
    - app/
      - api/v1/ (REST API endpoints with auth)
      - models/ (SQLAlchemy models)
      - services/ (Business logic - Facade)
      - persistence/ (SQLAlchemy repository)
    - instance/sql/ (SQL schema files)
    - tests/ (Test suite)
    - config.py (Application configuration)
    - run.py (Application entry point)
    - requirements.txt (Python dependencies)
    - README.md (Part 3 documentation)
  - part4/ (Phase 4 - Frontend Integration)
    - add_review.html (Review submission page)
    - index.html (Home page with places list)
    - login.html (Login page)
    - place.html (Place details page)
    - scripts.js (Main JavaScript with API calls)
    - styles.css (Application styles)
    - images/ (Images, logo, favicon)
    - README.md (Part 4 documentation)

## Implemented Features

### User Management
- User creation with validation
- Email uniqueness validation
- Password hashing with Bcrypt
- User authentication with JWT tokens
- User profile management (CRUD operations)

### Accommodation Management
- Place creation with validation
- Owner assignment and validation
- Price and location validation (latitude/longitude bounds)
- Place-amenity relationships (many-to-many)
- Place data retrieval and updates

### Amenity System
- Amenity creation and management
- Amenity-place associations
- Name validation and length constraints
- CRUD operations for amenities

### Review System
- Review creation with user and place validation
- Rating system (1-5 scale)
- Text validation
- Review retrieval and management
- CRUD operations for reviews

### Authentication and Security
- JWT token-based authentication
- Login endpoint with email/password validation
- Protected endpoints requiring valid tokens
- Password hashing with Bcrypt
- Role-based access control (is_admin flag)

### Database
- SQLAlchemy ORM with SQLite
- Database models with relationships
- One-to-many relationships (User-Places, User-Reviews, Place-Reviews)
- Many-to-many relationship (Place-Amenities)
- Database initialization script

## Development Status

### Part 1 - Design and Modeling (Completed)
- UML Diagrams: High-level package diagram, business logic layer diagram, sequence diagrams for API calls
- Architecture Decisions: Layered architecture, Facade pattern, Repository pattern, Security approach
- Flow Modeling: User creation, authentication, place creation, review creation flows
- Documentation: Comprehensive technical documentation

### Part 2 - Implementation with In-Memory Storage (Completed)
- Business Logic Layer: Complete model implementations, BaseModel, Facade pattern, In-memory repository
- REST API: Flask-RESTX based API, CRUD operations, Swagger UI documentation
- Architecture Implementation: Three-layer architecture, Repository pattern, Facade pattern
- Testing: Automated endpoint tests

### Part 3 - Database and Authentication (Completed)
- Database Integration: SQLAlchemy ORM, SQLite database, database models, SQL schema files
- Authentication System: JWT authentication, secure login, protected endpoints, role-based access
- Security Features: Bcrypt password hashing, JWT token signing, role-based authorization
- Database Relationships: User-Places, User-Reviews, Place-Reviews, Place-Amenities
- Repository Pattern: SQLAlchemy repository, specialized repositories
- Testing: Comprehensive tests for API, models, persistence

### Part 4 - Frontend Integration (Completed)
- Frontend Application: Static HTML/CSS/JavaScript interface, home page, login page, place details, review submission, JWT token management
- Backend API with CORS: Flask-CORS integration, separated backend API, support for frontend
- Pages Implemented: index.html, login.html, place.html, add_review.html
- JavaScript Features: API communication, authentication flow, dynamic content rendering
- Architecture: Separation between frontend and backend, RESTful API communication

## Technologies

### Backend
- Python 3.x
- Flask (Web framework)
- Flask-RESTX (REST API and automatic documentation)
- Flask-JWT-Extended (JWT authentication)
- Flask-Bcrypt (Password hashing)
- Flask-CORS (Cross-origin resource sharing)
- SQLAlchemy (ORM)
- Flask-SQLAlchemy (Flask-SQLAlchemy integration)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API for HTTP requests

### Database
- SQLite (Development and Testing)

### Architecture Patterns
- Facade Pattern (Business Logic simplification)
- Repository Pattern (Data access abstraction)
- Layered Architecture (Separation of concerns)

### Documentation
- Markdown for technical documentation

### Testing
- Unittest (Unit and integration testing)

## API Endpoints

### Authentication (Part 3)
- POST /api/v1/auth/login - Login with email and password, returns JWT token
- GET /api/v1/auth/protected - Protected endpoint requiring valid JWT token

### Users
- POST /api/v1/users/ - Create a new user
- GET /api/v1/users/ - Get all users
- GET /api/v1/users/<user_id> - Get a specific user
- PUT /api/v1/users/<user_id> - Update a user

### Places
- POST /api/v1/places/ - Create a new place
- GET /api/v1/places/ - Get all places
- GET /api/v1/places/<place_id> - Get a specific place
- PUT /api/v1/places/<place_id> - Update a place
- GET /api/v1/places/<place_id>/reviews - Get all reviews for a place

### Reviews
- POST /api/v1/reviews/ - Create a new review
- GET /api/v1/reviews/ - Get all reviews
- GET /api/v1/reviews/<review_id> - Get a specific review
- PUT /api/v1/reviews/<review_id> - Update a review
- DELETE /api/v1/reviews/<review_id> - Delete a review

### Amenities
- POST /api/v1/amenities/ - Create a new amenity
- GET /api/v1/amenities/ - Get all amenities
- GET /api/v1/amenities/<amenity_id> - Get a specific amenity
- PUT /api/v1/amenities/<amenity_id> - Update an amenity

### Common HTTP Status Codes
- 200 OK - Successful GET request
- 201 Created - Successful POST request
- 400 Bad Request - Invalid data or validation error
- 401 Unauthorized - Missing or invalid authentication token
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource not found

## About

Project developed as part of the Holberton School curriculum, applying software architecture concepts, web development, and programming best practices.

### Authors
- Part 1 (Design): Abbattista Morgane, Faroux Joan, Uzun Bengin
- Parts 2-3 (Implementation): Abbattista Morgane, Faroux Joan, Uzun Bengin
- Parts 4 (Web client service): Morgane Abbattista

### Key Learning Outcomes
- Layered architecture design and implementation
- RESTful API development with Flask-RESTX
- Authentication and security with JWT and Bcrypt
- Database design and ORM with SQLAlchemy
- Design patterns (Facade, Repository)
- Comprehensive testing strategies
- API documentation with Swagger

## Getting Started

To get started with the project:

1. Review Part 1 for architecture and design decisions
2. Run Part 2 to see the in-memory implementation
3. Deploy Part 3 for the full-stack application with database
4. Launch Part 4 for the complete application with frontend interface

Each part has detailed README files with setup instructions and documentation.

### Running Part 4 (Frontend + Backend)
```bash
# Backend (if not started): go to part3 and run API
cd part3
python3 run.py
# Backend runs on http://localhost:5000

# Frontend (in separate terminal)
cd ../part4
python3 -m http.server 8000
# Frontend runs on http://localhost:8000
```

## License

This project is developed for educational purposes as part of the Holberton School program.