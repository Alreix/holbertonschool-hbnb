/*
  Script for the login (task 01)
*/

document.addEventListener('DOMContentLoaded', () => {
  // Get the login form element by its ID
  const loginForm = document.getElementById('login-form');

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
});

// Asynchronous function to handle user login
async function loginUser (email, password) {
  // Define the login API endpoint URL
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
