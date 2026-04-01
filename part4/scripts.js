/*
  Login, Index, Place Details and Add Review
  This script handles:
  - login form submission
  - storing the JWT token in a cookie
  - showing or hiding the login link
  - fetching places for index.html
  - filtering places by price
  - fetching and displaying one place details
  - fetching and displaying place reviews
  - showing or hiding the add review section
  - submitting a review from add_review.html
*/

/**
 * Wait until the HTML page is fully loaded before running the code.
 * This avoids trying to access elements that are not ready yet.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Elements used on different pages
  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById('price-filter');
  const placeDetailsSection = document.getElementById('place-details');
  const reviewForm = document.getElementById('review-form');
  const logoutBtn = document.getElementById('logout-btn');

  // Setup logout button listener (available on all pages)
  if (logoutBtn) {
    logoutBtn.addEventListener('click', logoutUser);
  }

  /**
   * LOGIN PAGE LOGIC
   * If the login form exists, we are on login.html.
   */
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      // Prevent normal form submission and page reload
      event.preventDefault();

      // Get the email and password input fields
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');

      // Read user input values
      const email = emailInput.value.trim();
      const password = passwordInput.value;

      // Send credentials to the backend
      await loginUser(email, password);
    });
  }

  /**
   * INDEX PAGE LOGIC
   * If the price filter exists, we are on index.html.
   */
  if (priceFilter) {
    // Show or hide the Login link depending on authentication
    checkAuthentication();

    // Read the token from cookies and fetch places
    const token = getCookie('token');
    fetchPlaces(token);

    // Filter visible place cards when the selected price changes
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

    // Check authentication and update UI for this page
    checkAuthentication(placeId);

    // Update the Add Review link with the current place ID
    const addReviewLink = document.querySelector('#add-review a');
    if (addReviewLink && placeId) {
      addReviewLink.href = `add_review.html?id=${placeId}`;
    }

    // Fetch reviews for the current place
    fetchPlacesReviews(placeId);
  }

  /**
   * ADD REVIEW PAGE LOGIC
   * If the review form exists, we are on add_review.html.
   */
  if (reviewForm) {
    // Redirect to index.html if the user is not authenticated
    const token = checkAuthenticationForReview();

    // Get the place ID from the URL query string
    const placeId = getPlaceIdFromURL();

    // Listen for review form submission
    reviewForm.addEventListener('submit', async (event) => {
      // Prevent normal form submission and page reload
      event.preventDefault();

      // Get the review text and rating fields
      const reviewInput = document.getElementById('review');
      const ratingInput = document.getElementById('rating');

      // Read the user input values
      const reviewText = reviewInput.value.trim();
      const rating = ratingInput.value;

      // Send the review data to the backend
      await submitReview(token, placeId, reviewText, rating, reviewForm);
    });
  }
});

/**
 * Send login credentials to the backend login endpoint.
 * If login succeeds:
 * - read the returned JSON
 * - store the JWT token in a cookie
 * - redirect to index.html
 *
 * @param {string} email - Email entered by the user
 * @param {string} password - Password entered by the user
 */
async function loginUser (email, password) {
  const LOGIN_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

  try {
    const response = await fetch(LOGIN_URL, {
      method: 'POST',
      headers: {
        // Tell the backend the request body is JSON
        'Content-Type': 'application/json'
      },
      // Convert the JavaScript object into JSON text
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      // Convert backend JSON response into a JavaScript object
      const data = await response.json();

      // Store the JWT token in a cookie
      // path=/ makes the cookie available on all pages
      document.cookie = `token=${data.access_token}; path=/`;

      // Redirect after successful login
      window.location.href = 'index.html';
    } else {
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    alert('An error occurred while logging in.');
    console.error(error);
  }
}

/**
 * Logout the current user by removing the JWT token cookie.
 * This function clears the token and redirects to index.html.
 */
function logoutUser () {
  // Remove the token cookie by setting it to an empty string with an expired date
  document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;';

  // Redirect to index.html after logout
  window.location.href = 'index.html';
}

/**
 * Read a cookie value by its name.
 * This is used to get the JWT token stored after login.
 *
 * @param {string} name - Cookie name to search for
 * @returns {string|null} The cookie value if found, otherwise null
 */
function getCookie (name) {
  // Split all cookies into an array
  const cookies = document.cookie.split(';');

  // Check each cookie one by one
  for (let i = 0; i < cookies.length; i += 1) {
    const cookiePair = cookies[i].trim();

    // If the cookie starts with "name=", return only its value
    if (cookiePair.startsWith(`${name}=`)) {
      return cookiePair.substring(name.length + 1);
    }
  }

  // Return null if the cookie does not exist
  return null;
}

/**
 * Check if the user is authenticated by looking for the JWT token.
 * This function can be reused on several pages:
 * - index.html: show or hide the Login link
 * - place.html: show or hide the add review section
 * - place.html: fetch place details if a place ID is provided
 *
 * @param {string|null} placeId - Current place ID if on place.html
 * @returns {string|null} The JWT token if found, otherwise null
 */
function checkAuthentication (placeId = null) {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutBtn = document.getElementById('logout-btn');
  const addReviewSection = document.getElementById('add-review');

  // Update Login link visibility only if the element exists on the page
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  // Update Logout button visibility only if the element exists on the page
  if (logoutBtn) {
    if (!token) {
      logoutBtn.style.display = 'none';
    } else {
      logoutBtn.style.display = 'block';
    }
  }

  // Update Add Review visibility only if the element exists on the page
  if (addReviewSection) {
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
    }
  }

  // If we are on place.html and have a place ID, fetch its details
  if (placeId) {
    fetchPlaceDetails(token, placeId);
  }

  // Return the token so it can still be reused if needed
  return token;
}

/**
 * Fetch the list of places from the backend API.
 * If a token exists, include it in the Authorization header.
 *
 * @param {string|null} token - JWT token if the user is authenticated
 */
async function fetchPlaces (token) {
  const PLACES_URL = 'http://127.0.0.1:5000/api/v1/places/';

  const options = {
    method: 'GET',
    headers: {}
  };

  // Include the token only if it exists
  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(PLACES_URL, options);

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Create and display all place cards inside the places list section.
 *
 * @param {Array} places - Array of place objects returned by the backend
 */
function displayPlaces (places) {
  const placesList = document.getElementById('places-list');

  // Stop if the current page does not contain #places-list
  if (!placesList) {
    return;
  }

  // Clear the section before adding new cards
  placesList.innerHTML = '';

  // Loop through each place in the array
  places.forEach((place) => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';

    // Save the place price for later filtering
    placeCard.setAttribute('data-price', place.price);

    // Fill the card with place data
    placeCard.innerHTML = `
      <h2>${place.title}</h2>
      <p>${place.description || ''}</p>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    // Add the new card to the places list section
    placesList.appendChild(placeCard);
  });
}

/**
 * Filter the displayed place cards according to the selected max price.
 * If "all" is selected, all cards stay visible.
 *
 * @param {string} maxPrice - Selected value from the price filter
 */
function filterPlacesByPrice (maxPrice) {
  const placeCards = document.querySelectorAll('.place-card');

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
 * Extract the place ID from the URL query string.
 * Example:
 * place.html?id=12345 -> returns "12345"
 *
 * @returns {string|null} The place ID if found, otherwise null
 */
function getPlaceIdFromURL () {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/**
 * Fetch the details of one place from the backend API.
 * If a token exists, include it in the Authorization header.
 *
 * @param {string|null} token - JWT token if the user is authenticated
 * @param {string} placeId - ID of the place to fetch
 */
async function fetchPlaceDetails (token, placeId) {
  const PLACE_DETAILS_URL = `http://127.0.0.1:5000/api/v1/places/${placeId}`;
  const options = {
    method: 'GET',
    headers: {}
  };

  // Include the token only if it exists
  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(PLACE_DETAILS_URL, options);

    if (response.ok) {
      const place = await response.json();
      displayPlacesDetails(place);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Fetch the reviews of one place from the backend API.
 *
 * @param {string} placeId - ID of the place whose reviews must be fetched
 */
/**
 * Fetch user information by ID from the backend API.
 *
 * @param {string} userId - ID of the user to fetch
 * @returns {Promise<Object|null>} User object with first_name and last_name, or null if not found
 */
async function getUserInfo (userId) {
  const USER_URL = `http://127.0.0.1:5000/api/v1/users/${userId}`;

  try {
    const response = await fetch(USER_URL);

    if (response.ok) {
      return await response.json();
    }
  } catch (error) {
    console.error(`Error fetching user ${userId}:`, error);
  }

  return null;
}

async function fetchPlacesReviews (placeId) {
  const REVIEWS_URL = `http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`;

  try {
    const response = await fetch(REVIEWS_URL);

    if (response.ok) {
      const reviews = await response.json();

      // Fetch user info for all reviews in parallel
      const enrichedReviews = await Promise.all(
        reviews.map(async (review) => {
          const userInfo = await getUserInfo(review.owner_id);
          return {
            ...review,
            owner: userInfo
          };
        })
      );

      displayPlacesReviews(enrichedReviews);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Display the detailed information of one place inside #place-details.
 *
 * @param {Object} place - Place details returned by the backend
 */
function displayPlacesDetails (place) {
  const placeDetailsSection = document.getElementById('place-details');

  // Stop if the current page does not contain #place-details
  if (!placeDetailsSection) {
    return;
  }

  // Clear previous content before displaying the current place
  placeDetailsSection.innerHTML = '';

  // Create one container for place information
  const placeInfo = document.createElement('div');
  placeInfo.className = 'place-info';

  // Convert the amenities array into a readable text string
  const amenities = place.amenities.map((amenity) => amenity.name).join(', ');

  // Fill the place details block with backend data
  placeInfo.innerHTML = `
    <h1>${place.title}</h1>
    <p><strong>Host:</strong> ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown'}</p>
    <p><strong>Price per night:</strong> $${place.price}</p>
    <p><strong>Description:</strong> ${place.description || ''}</p>
    <p><strong>Amenities:</strong> ${amenities}</p>
  `;

  // Add the place details block to the page
  placeDetailsSection.appendChild(placeInfo);
}

/**
 * Display all reviews of the current place inside #reviews.
 *
 * @param {Array} reviews - Array of reviews returned by the backend (enriched with owner info)
 */
function displayPlacesReviews (reviews) {
  const reviewsSection = document.getElementById('reviews');

  // Stop if the current page does not contain #reviews
  if (!reviewsSection) {
    return;
  }

  // Keep the section title, then add the review cards
  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  reviews.forEach((review) => {
    const reviewCard = document.createElement('article');
    reviewCard.className = 'review-card';

    // Display user name if available, otherwise fall back to owner_id
    const userName = review.owner && review.owner.first_name && review.owner.last_name
      ? `${review.owner.first_name} ${review.owner.last_name}`
      : `User ${review.owner_id}`;

    reviewCard.innerHTML = `
      <p><strong>User:</strong> ${userName}</p>
      <p>${review.text}</p>
      <p><strong>Rating:</strong> ${review.rating}</p>
    `;

    reviewsSection.appendChild(reviewCard);
  });
}

/**
 * Check if the user is authenticated before accessing add_review.html.
 * If no token exists, redirect the user to index.html.
 *
 * @returns {string|null} The JWT token if found
 */
function checkAuthenticationForReview () {
  const token = getCookie('token');

  // Redirect unauthenticated users to index.html
  if (!token) {
    window.location.href = 'index.html';
  }
  if (loginLink) {
    loginLink.style.display = "none";
  }

  return token;
}

/**
 * Send a new review to the backend API.
 * The request includes:
 * - the JWT token in Authorization
 * - the review text
 * - the rating
 * - the place ID
 *
 * @param {string} token - JWT token of the authenticated user
 * @param {string} placeId - ID of the reviewed place
 * @param {string} reviewText - Text written by the user
 * @param {string} rating - Rating selected in the form
 * @param {HTMLFormElement} reviewForm - The review form element
 */
async function submitReview (token, placeId, reviewText, rating, reviewForm) {
  const REVIEW_URL = 'http://127.0.0.1:5000/api/v1/reviews/';

  try {
    const response = await fetch(REVIEW_URL, {
      method: 'POST',
      headers: {
        // Tell the backend that the request body is JSON
        'Content-Type': 'application/json',

        // Send the JWT token so the backend knows which user is submitting the review
        Authorization: `Bearer ${token}`
      },

      // Convert the review data into JSON text
      body: JSON.stringify({
        text: reviewText,
        rating: Number(rating),
        place_id: placeId
      })
    });

    // Handle success or failure after submission
    handleReviewResponse(response, reviewForm);
  } catch (error) {
    alert('An error occurred while submitting the review.');
    console.error(error);
  }
}

/**
 * Handle the backend response after submitting a review.
 * If the submission succeeds:
 * - show a success message
 * - reset the form
 * If it fails:
 * - show an error message
 *
 * @param {Response} response - Fetch response object
 * @param {HTMLFormElement} reviewForm - The submitted review form
 */
function handleReviewResponse (response, reviewForm) {
  if (response.ok) {
    alert('Review submitted successfully!');

    // Clear all fields in the form after success
    reviewForm.reset();
  } else {
    alert('Failed to submit review.');
  }
}
