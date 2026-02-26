// login scripts
document.getElementById('login-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const submitButton = document.querySelector('button[type="submit"]');
  
  submitButton.disabled = true;
  submitButton.textContent = 'Logging in...';
  
  const existingError = document.querySelector('.error-message');
  if (existingError) {
    existingError.remove();
  }
  
  // sample fetch request to server for authentication (will send an error for now until implemented)
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
      }),
      credentials: 'include'
    });
    
    const data = await response.json();
    
    if (response.ok && data.success) {
      window.location.href = '/';
    } else {
      showError(data.message || 'Invalid username or password');
      submitButton.disabled = false;
      submitButton.textContent = 'Login';
    }
  } catch (error) {
    console.error('Login error:', error);
    showError('An error occurred. Please try again.');
    submitButton.disabled = false;
    submitButton.textContent = 'Login';
  }
});

function showError(message) {
  const form = document.getElementById('login-form');
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;
  form.insertBefore(errorDiv, form.firstChild);
  
  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

window.addEventListener('load', function() {
  document.getElementById('login-form').reset();
});