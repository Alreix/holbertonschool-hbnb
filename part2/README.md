# HBnB - Part 2: Business Logic and REST API

## Introduction

Cette partie 2 du projet HBnB correspond à la phase d'implementation de l'application, a partir de l'architecture definie precedemment.
L'objectif est de construire une base fonctionnelle et evolutive avec Python, Flask et Flask-RESTX, en mettant en place:

- la couche Presentation (API REST)
- la couche Logique Metier (services + modeles)
- la couche Persistance (repository en memoire)

L'application met en oeuvre des principes d'architecture logicielle en couches, ainsi que les patterns **Facade** et **Repository** pour ameliorer la maintenabilite, la lisibilite et la scalabilite du code.

Note: l'authentification JWT et la gestion des roles ne sont pas traitees dans cette partie. Elles sont prevues pour la partie suivante.

---

## Project Objectives

- Construire une API modulaire avec Flask et Flask-RESTX.
- Implementer la logique metier des entites `User`, `Place`, `Amenity`, `Review`.
- Mettre en place une persistance en memoire via `InMemoryRepository`.
- Documenter les endpoints API (Swagger UI).
- Tester et valider les endpoints avec `unittest` et `cURL`.

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

Fichiers: `app/api/v1/*.py`

Responsabilites:
- definir les endpoints REST (`GET`, `POST`, `PUT`, `DELETE`)
- valider les payloads d'entree
- retourner des reponses JSON coherentes
- exposer une documentation Swagger via Flask-RESTX

URL de documentation:
- `http://127.0.0.1:5000/api/v1/`

### 2) Business Layer (Services / Facade)

Fichier: `app/services/facade.py`

Responsabilites:
- centraliser la logique metier dans `HBnBFacade`
- orchestrer les operations CRUD de toutes les entites
- valider les relations entre entites (owner, user, place, amenities)

### 3) Persistence Layer (Repository)

Fichier: `app/persistence/repository.py`

Responsabilites:
- stocker les objets en memoire
- fournir des operations communes: `add`, `get`, `get_all`, `update`, `delete`, `get_by_attribute`

### 4) Domain Models

Fichiers: `app/models/*.py`

Entites principales:
- `BaseModel`
- `User`
- `Place`
- `AmenityModel`
- `Review`

### 5) Configuration et Execution

- `config.py`: configuration generale de l'application
- `run.py`: point d'entree pour lancer le serveur
- `app/__init__.py`: factory Flask + enregistrement des namespaces API

---

## Main Features

### Users
- creation utilisateur
- recuperation liste/detail
- mise a jour profil
- verification unicite email

### Places
- creation de place avec owner existant
- ajout de liste d'amenities par IDs
- recuperation liste/detail
- mise a jour des attributs et relations
- endpoint des reviews d'une place

### Amenities
- creation amenity
- recuperation liste/detail
- mise a jour amenity

### Reviews
- creation review liee a un user/place existants
- recuperation liste/detail
- mise a jour review
- suppression review
- contraintes metier appliquees (validation des donnees, regles de relation)

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
- `cURL` commands (examples ci-dessus)

Points verifies:
- cas nominal
- validations de payload
- erreurs `400/404`
- relations entre entites
- regressions sur serialization des reponses

---

## Development Workflow

Workflow utilise:
- implementation par couche (models -> facade -> API)
- validation incrementale via `unittest`
- verification manuelle avec `cURL`
- mise a jour continue de la documentation (`README`)

---

## Authors

- HBnB Project Team
- Contributors: Faroux Joan, Abbattista Morgane, Uzun Bengin

---

## Notes

- Persistance en memoire uniquement.
- Un redemarrage du serveur reinitialise les donnees.
- Dependances minimales actuelles: `flask`, `flask-restx`.
