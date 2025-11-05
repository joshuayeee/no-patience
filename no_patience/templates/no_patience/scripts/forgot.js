document.getElementById('forgot-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const submitButton = document.querySelector('button[type="submit"]');
    
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    try {
        // implementation wont work unless backend is set up to handle forgot password requests
        const response = await fetch('/api/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('Password reset link sent to your email.');
            window.location.href = '/login';
        }
        else {
            showError(data.message || 'Error submitting request. Please try again.');
            submitButton.disabled = false;
            submitButton.textContent = 'Submit';
        }
    } catch (error) {
        console.error('Forgot password error:', error);
        showError('An error occurred. Please try again.');
        submitButton.disabled = false;
        submitButton.textContent = 'Submit';
    }
});

function showError(message) {
    const form = document.getElementById('forgot-form');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    form.insertBefore(errorDiv, form.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}