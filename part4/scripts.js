/*
  Script for login, index page and place details page
*/

// Store all fetched places for client-side filtering on index page
let allPlaces = [];

/**
 * Initialize page behavior when the DOM is fully loaded.
 * This block detects which page is currently open by checking
 * the existence of specific elements in the HTML.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Get elements used on different pages
  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById('price-filter');
  const placeDetailsSection = document.getElementById('place-details');
  const addReviewSection = document.getElementById('add-review');

  /**
   * LOGIN PAGE LOGIC
   * If the login form exists, we are on login.html.
   */
  if (loginForm) {
    // Listen for form submission
    loginForm.addEventListener('submit', async (event) => {
      // Prevent normal HTML form submission
      event.preventDefault();

      // Read user input values
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');

      // Clean the email and keep the password as typed
      const email = emailInput.value.trim();
      const password = passwordInput.value;

      // Send credentials to the API
      await loginUser(email, password);
    });
  }

  /**
   * INDEX PAGE LOGIC
   * If the price filter exists, we are on index.html.
   */
  if (priceFilter) {
    // Show or hide the login link depending on authentication
    checkAuthentication();

    // Read token from cookies and fetch places
    const token = getCookie('token');
    fetchPlaces(token);

    // Filter places when the selected max price changes
    priceFilter.addEventListener('change', (event) => {
      filterPlacesByPrice(event.target.value);
    });
  }

  /**
   * PLACE DETAILS PAGE LOGIC
   * If the place details section exists, we are on place.html.
   */
  if (placeDetailsSection) {
    // Extract the place ID from the URL
    const placeId = getPlaceIdFromURL();

    // Check authentication state for this page and get the token
    checkAuthentication(placeId);

    // Fetch place reviews for the current place
    fetchPlaceReviews(placeId);
  }
});

/**
 * Perform user login via API and store token in a cookie.
 * On success, redirect the user to index.html.
 *
 * @param {string} email
 * @param {string} password
 */
async function loginUser(email, password) {
  const LOGIN_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

  try {
    // Send credentials to the login endpoint
    const response = await fetch(LOGIN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    // If login is successful, save the JWT and redirect
    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
    } else {
      // Show a basic error message if authentication fails
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    // Show a generic message if the request fails completely
    alert('An error occurred while logging in.');
    console.error(error);
  }
}

/**
 * Read a cookie value by its name.
 *
 * @param {string} name
 * @returns {string|null}
 */
function getCookie(name) {
  // Split all cookies into an array
  const cookies = document.cookie.split(';');

  // Check each cookie one by one
  for (let i = 0; i < cookies.length; i += 1) {
    const cookiePair = cookies[i].trim();

    // Return the value if the cookie name matches
    if (cookiePair.startsWith(`${name}=`)) {
      return cookiePair.substring(name.length + 1);
    }
  }

  // Return null if the cookie does not exist
  return null;
}

/**
 * Check authentication state using the JWT token stored in cookies.
 * - On pages with a login link, show or hide it
 * - On place.html, show or hide the add review section
 * - If a placeId is provided, fetch place details with the token
 *
 * @param {string|null} placeId
 * @returns {string|null}
 */
function checkAuthentication(placeId = null) {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  // Show or hide the login link if it exists on the page
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  // Show or hide the add review section if it exists on the page
  if (addReviewSection) {
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
    }
  }

  // If we are on place.html and a place ID exists, fetch place details
  if (placeId) {
    fetchPlaceDetails(token, placeId);
  }

  // Return the token so it can still be reused if needed
  return token;
}

/**
 * Fetch the list of places from the API for index.html.
 * Includes the JWT token in Authorization if available.
 *
 * @param {string|null} token
 */
async function fetchPlaces(token) {
  const PLACE_URL = 'http://127.0.0.1:5000/api/v1/places/';
  const options = {
    method: 'GET',
    headers: {}
  };

  // Add Authorization header only if the token exists
  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(PLACE_URL, options);

    // If the API returns places successfully, display them
    if (response.ok) {
      const places = await response.json();
      allPlaces = places;
      displayPlaces(places);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Display all places dynamically inside #places-list.
 *
 * @param {Array} places
 */
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  // Prevent errors if the current page does not contain #places-list
  if (!placesList) {
    return;
  }

  // Remove previous content before adding new cards
  placesList.innerHTML = '';

  // Create one card per place
  places.forEach((place) => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';

    // Store the price in a custom attribute for filtering later
    placeCard.setAttribute('data-price', place.price);

    // Fill the card with place data
    placeCard.innerHTML = `
      <h2>${place.title}</h2>
      <p>${place.description || ''}</p>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    // Add the card to the places list
    placesList.appendChild(placeCard);
  });
}

/**
 * Filter place cards on index.html according to the selected max price.
 *
 * @param {string} maxPrice
 */
function filterPlacesByPrice(maxPrice) {
  const placeCards = document.querySelectorAll('.place-card');

  // Check each place card price and show/hide it
  placeCards.forEach((card) => {
    const price = Number(card.getAttribute('data-price'));

    if (maxPrice === 'all' || price <= Number(maxPrice)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

/**
 * Extract the place ID from the URL query parameters.
 * Example:
 * place.html?id=12345  -> returns "12345"
 *
 * @returns {string|null}
 */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/**
 * Fetch the details of one place from the API.
 * Includes the JWT token in Authorization if available.
 *
 * @param {string|null} token
 * @param {string|null} placeId
 */
async function fetchPlaceDetails(token, placeId) {
  // Stop if no place ID exists in the URL
  if (!placeId) {
    return;
  }

  const PLACE_DETAILS_URL = `http://127.0.0.1:5000/api/v1/places/${placeId}`;
  const options = {
    method: 'GET',
    headers: {}
  };

  // Add Authorization header only if a token exists
  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(PLACE_DETAILS_URL, options);

    // If the place details are returned correctly, display them
    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Fetch the reviews of one place from the API.
 *
 * @param {string|null} placeId
 */
async function fetchPlaceReviews(placeId) {
  // Stop if no place ID exists in the URL
  if (!placeId) {
    return;
  }

  const REVIEWS_URL = `http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`;

  try {
    const response = await fetch(REVIEWS_URL);

    // If the reviews are returned correctly, display them
    if (response.ok) {
      const reviews = await response.json();
      displayPlaceReviews(reviews);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Display detailed information about one place inside #place-details.
 * Shows the title, host, price, description and amenities.
 *
 * @param {Object} place
 */
function displayPlaceDetails(place) {
  const placeDetailsSection = document.getElementById('place-details');

  // Stop if the section does not exist
  if (!placeDetailsSection) {
    return;
  }

  // Prepare amenity names as a readable string
  const amenities = place.amenities.map((amenity) => amenity.name).join(', ');

  // Build the detailed place layout dynamically
  placeDetailsSection.innerHTML = `
    <div class="place-info">
      <h1>${place.title}</h1>
      <p><strong>Host:</strong> ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown'}</p>
      <p><strong>Price per night:</strong> $${place.price}</p>
      <p><strong>Description:</strong> ${place.description || ''}</p>
      <p><strong>Amenities:</strong> ${amenities}</p>
    </div>
  `;
}

/**
 * Display all reviews of the current place inside #reviews.
 *
 * @param {Array} reviews
 */
function displayPlaceReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');

  // Stop if the section does not exist
  if (!reviewsSection) {
    return;
  }

  // Keep the Reviews title, then inject the review cards
  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  reviews.forEach((review) => {
    const reviewCard = document.createElement('article');
    reviewCard.className = 'review-card';

    // Build one review card
    reviewCard.innerHTML = `
      <p><strong>User:</strong> ${review.owner_id}</p>
      <p>${review.text}</p>
      <p><strong>Rating:</strong> ${review.rating}</p>
    `;

    reviewsSection.appendChild(reviewCard);
  });
}