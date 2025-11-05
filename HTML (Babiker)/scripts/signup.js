// signup scripts

// Fetch and populate locations on page load
async function loadLocations() {
  const locationSelect = document.getElementById("location");
  locationSelect.innerHTML = '<option value="">Loading locations...</option>';

  // sample location data fetch (will not populate until implemented fully)
  try {
    const response = await fetch("/api/locations");
    const data = await response.json();

    if (response.ok && data.locations) {
      locationSelect.innerHTML =
        '<option value="">Select your location</option>';
      data.locations.forEach((loc) => {
        const option = document.createElement("option");
        option.value = loc.id;
        option.textContent = loc.name;
        locationSelect.appendChild(option);
      });
    } else {
      locationSelect.innerHTML =
        '<option value="">Failed to load locations</option>';
    }
  } catch (error) {
    console.error("Error loading locations:", error);
    locationSelect.innerHTML =
      '<option value="">Error loading locations...</option>';
  }
}

document
  .getElementById("signup-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const location = document.getElementById("location").value;
    const submitButton = document.querySelector('button[type="submit"]');

    submitButton.disabled = true;
    submitButton.textContent = "Signing up...";

    const existingError = document.querySelector(".error-message");
    if (existingError) {
      existingError.remove();
    }

    // sample fetch request to server for registration (will send an error for now until implemented)
    try {
      const response = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
          location: location,
        }),
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok && data.success) {
        window.location.href = "/login";
      } else {
        showError(data.message || "Signup failed. Please try again.");
        submitButton.disabled = false;
        submitButton.textContent = "Sign Up";
      }
    } catch (error) {
      console.error("Signup error:", error);
      showError("An error occurred. Please try again.");
      submitButton.disabled = false;
      submitButton.textContent = "Sign Up";
    }
  });

function showError(message) {
  const form = document.getElementById("signup-form");
  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";
  errorDiv.textContent = message;
  form.insertBefore(errorDiv, form.firstChild);

  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

window.addEventListener("load", function () {
  document.getElementById("signup-form").reset();
  loadLocations();
});
