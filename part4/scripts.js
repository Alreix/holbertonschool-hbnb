/*
  Script for login and index page
*/

let allPlaces = [];

/**
 * Initialize page behavior when DOM is ready:
 * - login form submission handling
 * - loading places and filtering behavior
 */
document.addEventListener('DOMContentLoaded', () => {
  // Get the login form element by its ID
  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById('price-filter');

  if (loginForm) {
    // Add an event listener for the form submission
    loginForm.addEventListener('submit', async (event) => {
      // Prevent the default form submission behavior (page reload)
      event.preventDefault();

      // Get the email and password input elements
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');

      // Get the trimmed email value and password value
      const email = emailInput.value.trim();
      const password = passwordInput.value;

      // Call the loginUser function with the email and password
      await loginUser(email, password);
    });
  }

  if (priceFilter) {
    checkAuthentication();

    const token = getCookie('token');
    fetchPlaces(token);

    priceFilter.addEventListener('change', (event) => {
      filterPlacesByPrice(event.target.value);
    });
  }
});

/**
 * Perform user login via API and store token cookie.
 * @param {string} email
 * @param {string} password
 */
async function loginUser (email, password) {
  const LOGIN_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

  try {
    // Send a POST request to the login API with email and password
    const response = await fetch(LOGIN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    // Check if the response is successful (status 200-299)
    if (response.ok) {
      // Parse the JSON response data
      const data = await response.json();
      // Store the access token in a cookie for session management
      document.cookie = `token=${data.access_token}; path=/`;
      // Redirect to the index page after successful login
      window.location.href = 'index.html';
    } else {
      // Alert the user if login failed with the response status text
      alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    // Alert the user if an error occurred during the login process
    alert('An error occurred while logging in.');
    console.error(error);
  }
}

/**
 * Read a cookie value by name.
 * @param {string} name
 * @returns {string|null}
 */
function getCookie (name) {
  const cookies = document.cookie.split(';');

  for (let i = 0; i < cookies.length; i += 1) {
    const cookiePair = cookies[i].trim();
    if (cookiePair.startsWith(`${name}=`)) {
      return cookiePair.substring(name.length + 1);
    }
  }

  return null;
}

/**
 * Check login state and toggle login link visibility.
 */
function checkAuthentication () {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
  }
}

/**
 * Fetch place listings from API, then display them.
 * @param {string|null} token
 */
async function fetchPlaces (token) {
  const PLACE_URL = 'http://127.0.0.1:5000/api/v1/places/';
  const options = {
    method: 'GET',
    headers: {}
  };

  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(PLACE_URL, options);

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
 * Display all places dynamically inside the places list section.
 * @param {Array} places
 */
function displayPlaces (places) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list
  const placesList = document.getElementById('places-list');

  placesList.innerHTML = '';

  places.forEach((place) => {
    const placeCard = document.createElement('article');
    placeCard.className = 'place-card';
    placeCard.setAttribute('data-price', place.price);

    placeCard.innerHTML = `
      <h2>${place.title}</h2>
      <p>${place.description || ''}</p>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(placeCard);
  });
}

/**
 * Filter visible place cards based on selected max price.
 * @param {string} maxPrice
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
