# HBnB - Holberton Project

> A progressive Airbnb-like accommodation platform built during the Holberton School curriculum, from technical design to backend API, database persistence, authentication and frontend integration.

---

## Project Description

HBnB is a progressive accommodation platform built from a learning roadmap at Holberton School.

The project progresses through several phases:

* technical design and architecture planning;
* backend implementation with RESTful API endpoints;
* database persistence with SQLAlchemy;
* authentication and authorization with JWT;
* frontend integration using HTML, CSS and JavaScript.

The goal of this project is to understand how a web application can be structured with clear separation of responsibilities between the presentation layer, business logic and persistence layer.

---

## Objectives

* Provide a modular design based on separated responsibilities.
* Build RESTful operations for core resources: users, places, amenities and reviews.
* Implement a business layer controller and decoupled persistence.
* Add secure access with JSON Web Tokens and password hashing.
* Link frontend interactions to the API for a complete user flow.
* Practice clean architecture, API design, authentication and database modeling.

---

## Architecture

The project follows a layered architecture.

### Layers and roles

* **Presentation layer**: HTTP API endpoints in the application packages.
* **Business layer**: service and facade components for domain rules.
* **Persistence layer**: in-memory repository for early phases, then SQLAlchemy for database persistence.
* **Database engine**: SQLite with model relationships.

### Architecture patterns

* Facade pattern for service orchestration.
* Repository abstraction for data access.
* Layered separation for maintainability.
* Model-based data validation and relationships.

---

## Project Structure

```text
holbertonschool-hbnb/
├── part1/                          # Phase 1 - Design
│   └── TECHNICAL_DOCUMENTATION.md  # Technical documentation with UML diagrams
│
├── part2/                          # Phase 2 - Implementation with in-memory storage
│   ├── app/                        # Application package
│   │   ├── api/v1/                 # REST API endpoints
│   │   ├── models/                 # Data models
│   │   ├── services/               # Business logic (Facade)
│   │   └── persistence/            # In-memory persistence layer
│   ├── tests/                      # Test suite
│   ├── config.py                   # Application configuration
│   ├── run.py                      # Application entry point
│   ├── requirements.txt            # Python dependencies
│   └── README.md                   # Part 2 documentation
│
├── part3/                          # Phase 3 - Database and Authentication
│   ├── app/                        # Application package
│   │   ├── api/v1/                 # REST API endpoints with authentication
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── services/               # Business logic (Facade)
│   │   └── persistence/            # SQLAlchemy repository
│   ├── instance/sql/               # SQL schema files
│   ├── tests/                      # Test suite
│   ├── config.py                   # Application configuration
│   ├── run.py                      # Application entry point
│   ├── requirements.txt            # Python dependencies
│   └── README.md                   # Part 3 documentation
│
└── part4/                          # Phase 4 - Frontend Integration
    ├── add_review.html             # Review submission page
    ├── index.html                  # Home page with places list
    ├── login.html                  # Login page
    ├── place.html                  # Place details page
    ├── scripts.js                  # Main JavaScript file with API calls
    ├── styles.css                  # Application styles
    ├── images/                     # Images, logo and favicon
    └── README.md                   # Part 4 documentation
```

---

## Implemented Features

### User Management

* User registration handles field validation and uniqueness.
* Passwords are hashed with bcrypt before storing.
* Login issues a JWT token for secured endpoint access.
* User profile access and updates are protected.

### Place Management

* Place operations include creation, listing, update and deletion.
* Ownership verification and location bounds are applied.
* Amenity attachments can be managed on places.

### Amenity Management

* Amenity CRUD paths are available.
* Name constraints prevent duplicates and invalid entries.

### Review Management

* Users can create reviews associated with a place.
* Ratings and text are validated with clear boundaries.
* Review editing and removal are limited to owner/admin roles.

### Security

* API endpoints use JWT validation for protected routes.
* Passwords are hashed before being stored.
* Admin status and ownership are checked before updates and deletions.
* API access rules are implemented through authentication and authorization logic.

### Persistence

* Part 2 relies on an in-memory repository for fast iteration.
* Part 3 and Part 4 use SQLAlchemy with SQLite persistence.

---

## Development Status

### Part 1 - Design and Modeling

Status: completed.

* Designed architecture and workflows by mapping use cases.
* Documented entity relationships and process flows.
* Defined interfaces for facade and repository roles.

### Part 2 - Implementation with In-Memory Storage

Status: completed.

* Implemented models, service facade and in-memory repository.
* Added API routes with validation and error handling.
* Includes automated tests for API and business rules.

### Part 3 - Database and Authentication

Status: completed.

* Implemented SQLAlchemy models and database persistence.
* Added JWT authentication and protected routes.
* Developed role-based access checks and repository patterns.

### Part 4 - Frontend Integration

Status: completed.

* Implemented static UI pages: home page, login page, place details page and review submission page.
* Connected frontend to backend API using JavaScript `fetch`.
* Added CORS support and client-side interactions.

---

## Technologies Used

### Backend

* Python 3.x
* Flask
* Flask-RESTX
* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-CORS
* SQLAlchemy
* Flask-SQLAlchemy
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript ES6+
* Fetch API

### Database

* SQLite for local development and test runs.
* SQLAlchemy ORM for model relationships and persistence.

### Testing and Quality

* `unittest` for unit and integration tests.
* `pycodestyle` for Python style checking.

---

## Prerequisites

Before running this project, make sure you have the following installed:

* Ubuntu 20.04 LTS or later, or another Linux-based environment
* Python 3.x
* `pip`
* `venv`
* SQLite
* Git
* A modern web browser for the frontend part

Recommended Python version:

```bash
python3 --version
```

Recommended pip version:

```bash
pip3 --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Alreix/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

Go to the backend part:

```bash
cd part3
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python3 init_db.py
```

---

## Usage

### Run the backend API

From the `part3` directory, start the backend server:

```bash
python3 run.py
```

The API is available at:

```text
http://127.0.0.1:5000/api/v1
```

### Example API request

Example request to list places:

```bash
curl http://127.0.0.1:5000/api/v1/places/
```

Example request to list users:

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

### Run the frontend

Open another terminal and go to the frontend part:

```bash
cd holbertonschool-hbnb/part4
```

Start a local HTTP server:

```bash
python3 -m http.server 8000
```

Then open the frontend in your browser:

```text
http://localhost:8000
```

---

## API Endpoints

The base API path is:

```text
/api/v1
```

### Authentication

| Method | Endpoint                 | Description                                            |
| ------ | ------------------------ | ------------------------------------------------------ |
| `POST` | `/api/v1/auth/login`     | Authenticates user credentials and returns a JWT token |
| `GET`  | `/api/v1/auth/protected` | Protected endpoint requiring a valid JWT token         |

### Users

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| `POST` | `/api/v1/users/`          | Register a new user      |
| `GET`  | `/api/v1/users/`          | List users               |
| `GET`  | `/api/v1/users/<user_id>` | Get details for one user |
| `PUT`  | `/api/v1/users/<user_id>` | Update user profile      |

### Places

| Method | Endpoint                            | Description             |
| ------ | ----------------------------------- | ----------------------- |
| `POST` | `/api/v1/places/`                   | Create a new place      |
| `GET`  | `/api/v1/places/`                   | Retrieve all places     |
| `GET`  | `/api/v1/places/<place_id>`         | Retrieve one place      |
| `PUT`  | `/api/v1/places/<place_id>`         | Modify a place          |
| `GET`  | `/api/v1/places/<place_id>/reviews` | Get reviews for a place |

### Reviews

| Method   | Endpoint                      | Description         |
| -------- | ----------------------------- | ------------------- |
| `POST`   | `/api/v1/reviews/`            | Create a new review |
| `GET`    | `/api/v1/reviews/`            | Get all reviews     |
| `GET`    | `/api/v1/reviews/<review_id>` | View one review     |
| `PUT`    | `/api/v1/reviews/<review_id>` | Edit a review       |
| `DELETE` | `/api/v1/reviews/<review_id>` | Delete a review     |

### Amenities

| Method | Endpoint                         | Description          |
| ------ | -------------------------------- | -------------------- |
| `POST` | `/api/v1/amenities/`             | Create a new amenity |
| `GET`  | `/api/v1/amenities/`             | List amenities       |
| `GET`  | `/api/v1/amenities/<amenity_id>` | Get amenity details  |
| `PUT`  | `/api/v1/amenities/<amenity_id>` | Update amenity       |

---

## Common HTTP Status Codes

| Status Code        | Meaning                          |
| ------------------ | -------------------------------- |
| `200 OK`           | Request succeeded                |
| `201 Created`      | Resource created                 |
| `400 Bad Request`  | Input validation or format error |
| `401 Unauthorized` | Missing or invalid token         |
| `403 Forbidden`    | Access right denied              |
| `404 Not Found`    | Resource missing                 |

---

## Screenshots

Screenshots are not required for the backend API part of this project.

The frontend part contains static HTML/CSS pages connected to the backend API, including:

* a home page displaying places;
* a login page;
* a place details page;
* a review submission page.

Screenshots can be added later in a `docs/` or `screenshots/` directory if needed.

---

## Testing

Run tests from the relevant project part.

Example for Part 3:

```bash
cd part3
python3 -m unittest discover tests
```

The test suite checks API behavior, validation rules, authentication logic and business rules.

---

## Code Quality

Python code should be checked with `pycodestyle`:

```bash
pycodestyle .
```

The project follows Holberton School coding expectations:

* clear function and variable names;
* modular file organization;
* separation between routes, models, services and persistence;
* explicit validation and error handling;
* no useless generated files committed to the repository.

---

## Documentation Standard

Python modules, classes and functions are documented with docstrings following the Holberton School Python documentation style.

The codebase aims to keep documentation clear and useful:

* modules describe their purpose;
* classes describe their responsibility;
* functions and methods describe what they do, their expected parameters and return values when relevant;
* comments are used only when they help explain non-obvious logic.

---

## Git Hygiene

Generated files and local environment files should not be committed.

The repository should ignore files such as:

* `.DS_Store`
* `__pycache__/`
* `*.pyc`
* `.env`
* `venv/`
* local database files
* editor configuration folders when not needed

A `.gitignore` file should be used to keep the repository clean.

Recommended `.gitignore` content:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
venv/
env/
.env

# Database
*.db
*.sqlite
*.sqlite3

# OS files
.DS_Store

# Editors
.vscode/
.idea/

# Logs
*.log
```

---

## Branch Strategy

This repository uses the following branch strategy:

* `main`: stable version used for final delivery;
* `dev`: development branch used before merging into `main`.

Feature or fix work should be done in dedicated branches, then merged into `dev` before being merged into `main`.

This strategy helps separate stable code from ongoing development work.

---

## Contributions and Acknowledgements

This project was completed as part of the Holberton School curriculum.

### Authors

* Abbattista Morgane
* Faroux Joan
* Uzun Bengin

Thanks to Holberton School for the project guidelines and learning framework.

---

## License

Project produced for academic evaluation at Holberton School.
