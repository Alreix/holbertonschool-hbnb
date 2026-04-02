# HBNB - Simple Web Client

## Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Frontend Usage](#frontend-usage)
- [API Endpoints](#api-endpoints)
- [Technical Implementation](#technical-implementation)
- [Authentication](#authentication)
- [Author](#author)

## Overview

HBNB is a web-based accommodation listing platform frontend built with HTML5, CSS3, and JavaScript ES6. This component serves as the user interface layer, connecting to a RESTful API backend developed in Part 3 of the project. The frontend provides a modern, responsive user experience for browsing accommodations, managing reviews, and handling user authentication.

## Objectives

The primary objectives of this frontend implementation are:

- Develop a user-friendly interface following modern web design specifications
- Implement client-side functionality to communicate with the RESTful API backend
- Ensure secure and efficient data handling using JavaScript ES6
- Apply contemporary web development practices to create a dynamic web application
- Provide seamless user authentication and session management
- Implement client-side filtering and navigation without page reloads

## Features

### Authentication Management

- Login functionality with email and password validation
- JWT token-based session management stored in secure cookies
- Automatic logout with session clearing
- Protected routes that redirect unauthenticated users to login
- Dynamic UI elements that show/hide based on authentication status

### Place Listing and Discovery

- Display comprehensive list of all available accommodations
- Real-time filtering by maximum price with instant visual updates
- Responsive card layout that adapts to different screen sizes
- Hover effects and smooth transitions for enhanced interactivity
- Quick access to detailed place information

### Place Details

- Complete accommodation information display
- Dynamic place ID routing from URL query parameters
- Detailed amenities and pricing information
- Review section with user feedback
- Conditional access to review submission for authenticated users

### Review Management

- Display existing reviews with user information (full names instead of IDs)
- Asynchronous user data enrichment for enhanced display
- Review submission form accessible only to authenticated users
- Form validation and error handling
- Automatic redirection to index page for unauthorized access

### Modern User Interface

- Professional design with modern typography and color scheme
- Consistent spacing and visual hierarchy throughout
- Smooth animations and transitions (0.3s cubic-bezier)
- Subtle shadows and depth for visual appeal
- Fully responsive design for mobile, tablet, and desktop devices
- Optimized performance with minimal layout shifts

## Architecture

The frontend follows a client-side MVC-inspired architecture:

```
HTML (Structure)
  |
CSS (Presentation) ← Modern, organized stylesheets with CSS variables
  |
JavaScript (Behavior) ← ES6 with async/await, Fetch API
  |
REST API Backend (Part 3) ← Flask application
```

### Technology Stack

- **HTML5**: Semantic markup for accessibility and SEO
- **CSS3**: Grid layout, flexbox, CSS variables for theming, media queries
- **JavaScript ES6**: Arrow functions, async/await, template literals, fetch API
- **Authentication**: JWT tokens in HTTP-only cookies
- **Communication**: Fetch API for HTTP requests

## Project Structure

```
part4/
├── index.html                 # Main places listing page
├── place.html                 # Individual place details page
├── login.html                 # User authentication form
├── add_review.html            # Review submission form
├── styles.css                 # Centralized stylesheet with responsive design
├── scripts.js                 # All client-side JavaScript logic
├── README.md                  # Documentation
└── requirements.txt           # Python dependencies
```

### File Descriptions

**HTML Files:**
- `index.html`: Displays all accommodations with price filtering functionality
- `place.html`: Shows detailed information for a specific accommodation with reviews
- `login.html`: Provides authentication interface for user login
- `add_review.html`: Contains form for submitting reviews on accommodations

**Styling:**
- `styles.css`: Unified stylesheet incorporating global styles, typography, layouts, components, and responsive breakpoints

**JavaScript:**
- `scripts.js`: Central event handling, API communication, DOM manipulation, and business logic

## Backend Setup

The frontend requires the backend API server to be running. The backend is located in Part 3 of this project.

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment

### Installation and Startup

1. Navigate to the Part 3 directory:

```bash
cd ../part3
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database:

```bash
python init_development_db.sql
```

5. Start the backend server:

```bash
python run.py
```

The API server will be available at `http://localhost:5000`

### Expected Backend Output

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Frontend Usage

No installation is required for the frontend. Simply open the HTML files in a web browser or use a local web server.


### User Flow

1. **Initial Access**: User arrives at the login page if not authenticated
2. **Authentication**: User enters credentials to receive JWT token
3. **Browse**: User views available accommodations with price filtering
4. **Explore**: User clicks "View Details" to see full place information
5. **Review**: Authenticated users can submit reviews for accommodations
6. **Logout**: User can securely logout to clear session

## API Endpoints

The frontend communicates with the following backend endpoints:

### Authentication

- `POST /api/v1/auth/login`
  - Request: `{ "email": "string", "password": "string" }`
  - Response: `{ "access_token": "string" }`
  - Purpose: User authentication and JWT token generation

### Places

- `GET /api/v1/places`
  - Response: Array of place objects
  - Purpose: Retrieve all available accommodations

- `GET /api/v1/places/{place_id}`
  - Response: Place object with details
  - Purpose: Fetch specific accommodation information

### Users

- `GET /api/v1/users/{user_id}`
  - Response: User object with profile information
  - Purpose: Retrieve user details for review attribution

### Reviews

- `GET /api/v1/places/{place_id}/reviews`
  - Response: Array of review objects for the place
  - Purpose: Fetch all reviews for a specific accommodation

- `POST /api/v1/places/{place_id}/reviews`
  - Request: `{ "text": "string", "rating": "integer" }`
  - Response: Newly created review object
  - Purpose: Submit a review for an accommodation

## Technical Implementation

### Authentication Flow

1. User submits credentials via login form
2. JavaScript sends POST request to `/api/v1/auth/login`
3. Backend returns JWT access token
4. Frontend stores token in secure HTTP-only cookie
5. Token automatically included in subsequent API requests
6. Token validation checked on page load via `checkAuthentication()`

### Data Fetching Strategy

The frontend uses the Fetch API with async/await pattern:

```javascript
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('API request failed');
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
  }
}
```

### Asynchronous User Data Enrichment

Reviews display full user names instead of IDs through parallel data fetching:

```javascript
const enrichedReviews = await Promise.all(
  reviews.map(async (review) => {
    const user = await getUserInfo(review.owner_id);
    return { ...review, userName: user.first_name + ' ' + user.last_name };
  })
);
```

### Client-Side Filtering

Price filtering operates on cached DOM elements without page reload:

```javascript
function filterPlacesByPrice(maxPrice) {
  document.querySelectorAll('.place-card').forEach(card => {
    const price = parseFloat(card.getAttribute('data-price'));
    card.style.display = (maxPrice === 'all' || price <= maxPrice) ? 'block' : 'none';
  });
}
```


## Authentication

### Security Considerations

- JWT tokens stored in HTTP-only cookies to prevent XSS attacks
- Automatic token validation on page initialization
- Silent token refresh on protected pages
- Logout functionality clears all session data
- Unauthenticated users cannot access protected routes

### Session Management

- Tokens persist across page reloads (stored in cookies)
- Session validation occurs automatically on frontend initialization
- User logout immediately clears state and redirects to home
- Protected pages check token before rendering authenticated content

## CORS Configuration

When running frontend and backend on different origins, CORS headers must be configured. If encountering CORS errors:

1. Ensure backend API includes proper CORS headers:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

2. Verify API server is running on `http://localhost:5000`

3. Clear browser cache and reload page

## Error Handling

The application implements comprehensive error handling:

- Network errors display informative messages
- Invalid authentication redirects to login
- Missing data gracefully degrades with default values
- Form validation prevents invalid submissions
- API errors are logged to browser console for debugging

## Author

**Morgane Abbattista**

- GitHub: [@Alreix](https://github.com/Alreix)
- Project: Holberton School - HBNB Web Client
- Part 4: Simple Web Client Implementation
