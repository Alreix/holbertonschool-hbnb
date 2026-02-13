# HBnB Evolution – Technical Documentation  
## Part 1: Architecture and Design

---

## 1. Introduction

HBnB Evolution is a simplified AirBnB-like application designed to manage users, places, reviews, and amenities. The application allows users to register and manage their profiles, create and manage place listings, submit reviews for places, and retrieve a list of available places based on search criteria.

The purpose of this technical document is to compile and explain the UML diagrams produced during Part 1 of the project. It serves as a technical blueprint that describes the architecture, the business logic design, and the interaction flows between system components. This document is intended to guide the implementation phases of the HBnB Evolution application and to provide a clear reference for understanding the system’s structure and behavior.

This document includes:
- A high-level overview of the system architecture  
- A detailed description of the Business Logic layer and its entities  
- Sequence diagrams illustrating the main API interaction flows  

---

## 2. High-Level Architecture

### 2.1 Layered Architecture Overview

HBnB Evolution follows a **three-layer architecture**:

#### Presentation Layer
This layer exposes the API endpoints through which clients interact with the system. It receives requests, forwards them to the Business Logic layer, and returns appropriate responses.

#### Business Logic Layer
This layer contains the core logic of the application. It validates input data, applies business rules, manages entity lifecycles, and coordinates interactions with the persistence layer.

#### Persistence Layer
This layer is responsible for storing and retrieving data from the database using repository components.

This layered structure ensures a clear separation of responsibilities and improves maintainability and clarity.

---

### 2.2 Facade Pattern

Communication between the Presentation Layer and the Business Logic Layer is handled using a **Facade pattern**.

The Facade:
- Acts as a single entry point for API calls  
- Centralizes access to business logic  
- Prevents direct interaction between the API and persistence components  

This design simplifies the Presentation Layer and helps keep business logic isolated and consistent.

---

### 2.3 High-Level Package Diagram

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    User
    Place
    Amenity
    Review
}

class BusinessLogicLayer {
    UserModel
    PlaceModel
    ReviewModel
    AmenityModel
}

class PersistenceLayer {
    Database
    User_repository
    Place_repository
    Review_repository
    Amenity_repository
}

PresentationLayer ..> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer ..> PersistenceLayer : Database Operations
```

### Explanatory Notes

- The Presentation Layer depends only on the Business Logic Layer through the Facade.

- Business logic is isolated from database concerns.

- The Persistence Layer provides database access through repositories.

## 3. Business Logic Layer
## 3.1 Overview
The Business Logic layer defines the main entities of the application and the relationships between them. It is responsible for enforcing business rules and managing entity lifecycles.

All entities:

- Are uniquely identified by a UUID

- Store creation and update timestamps

- Expose basic lifecycle operations (create, update, delete)

---

## 3.2 Core Entities

### User
Represents a system user.

#### Key attributes

- id (uuid)

- name

- lastname

- email

- password

- created_at

- updated_at

- is_admin

A user can own places and write reviews.

---

### Place
Represents a property listed by a user.

#### Key attributes

- id (uuid)

- title

- description

- price

- latitude

- longitude

- created_at

- updated_at

A place belongs to a single user and can include amenities and receive reviews.

---

### Review
Represents feedback left by a user for a place.

#### Key attributes

- id (uuid)

- rating

- comment

- created_at

- updated_at

A review is associated with one user and one place.

---

### Amenity
Represents a feature or service associated with a place.

#### Key attributes

- id (uuid)

- name

- description

- created_at

- updated_at

An amenity can be associated with multiple places.

---

### 3.3 Business Logic Class Diagram

```mermaid
classDiagram
direction LR

class User {
    id: uuid
    name: string
    lastname: string
    email: string
    password: string
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    create()
    update()
    delete()
}

class Place {
    id: uuid
    title: string
    description: string
    price: float
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime
    create()
    update()
    delete()
}

class Review {
    id: uuid
    rating: int
    comment: string
    created_at: datetime
    updated_at: datetime
    create()
    update()
    delete()
}

class Amenity {
    id: uuid
    name: string
    description: string
    created_at: datetime
    updated_at: datetime
    create()
    update()
    delete()
}

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : has
Place "*" -- "*" Amenity : includes
```

#### Explanatory Notes

- Relationships enforce ownership and responsibility between entities.

- UUIDs ensure unique identification.

- Timestamps allow tracking entity creation and updates.

---

## 4. API Interaction Flow
This section presents the sequence diagrams for the main API calls. Each diagram illustrates the interaction between the Presentation, Business Logic, and Persistence layers, as well as the flow of information through the system.

---

### 4.1 User Registration
#### Purpose
Allows a new user to register an account.

```mermaid
sequenceDiagram
autonumber
participant U as User (Client)
participant API as API (Presentation)
participant FAC as HBnBFacade (Business)
participant SVC as UserService (Business)
participant REPO as UserRepository (Persistence)
participant DB as Database (Persistence)

U->>API: POST /users
API->>API: Validate required fields
alt invalid data
    API-->>U: 400 Bad Request
else valid data
    API->>FAC: register_user
    FAC->>SVC: register_user
    SVC->>REPO: find_by_email
    REPO->>DB: SELECT user
    alt email exists
        API-->>U: 409 Conflict
    else email not found
        SVC->>REPO: create_user
        REPO->>DB: INSERT user
        API-->>U: 201 Created
    end
end
```

#### Explanation
This sequence shows validation of user data, email uniqueness checking, and user creation with UUID and timestamps before persistence.

---

### 4.2 Place Creation
#### Purpose
Allows an authenticated user to create a place listing.

```mermaid
sequenceDiagram
autonumber
participant U as User
participant API as API
participant FAC as Facade
participant PM as PlaceModel
participant REPO as Repo
participant DB as DB

U->>API: POST /places
API->>FAC: check_token
alt invalid token
    API-->>U: 401 Unauthorized
else valid token
    FAC->>PM: validate place data
    alt invalid data
        API-->>U: 400 Bad Request
    else valid data
        PM->>REPO: create place
        REPO->>DB: INSERT place
        API-->>U: 201 Created
    end
end
```

#### Explanation
This flow highlights authentication, place data validation, conflict checking, and persistence.

---

### 4.3 Review Submission
#### Purpose
Allows a user to submit a review for a place.

```mermaid
sequenceDiagram
autonumber
participant U as User
participant API as API
participant F as Facade
participant RM as ReviewModel
participant R as Repo
participant DB as DB

U->>API: POST /reviews
API->>F: validate_token
alt invalid token
    API-->>U: 401 Unauthorized
else valid token
    F->>RM: create_review
    RM->>R: verify place
    alt place not found
        API-->>U: 404 Not Found
    else place exists
        RM->>R: save review
        R->>DB: INSERT review
        API-->>U: 201 Created
    end
end
```

#### Explanation
This sequence ensures authentication, place existence verification, review validation, and persistence.

---

### 4.4 Fetching a List of Places
#### Purpose
Retrieves a list of places matching search criteria.

```mermaid
sequenceDiagram
autonumber
participant C as User
participant API as API
participant F as Facade
participant PM as PlaceModel
participant R as Repo
participant DB as DB

C->>API: GET /places
API->>F: list_places
F->>PM: validate filters
alt invalid filters
    API-->>C: 400 Bad Request
else valid filters
    PM->>R: find_places
    R->>DB: SELECT places
    API-->>C: 200 OK
end
```

#### Explanation
This flow illustrates filter validation, database querying, and returning a list of places (which may be empty).

---

### About This Work
Created by Joan Faroux, Morgane Abbattista, Bengin Uzun
Holberton School Project – Part 1
