// signup scripts

// Fetch and populate locations on page load
async function loadLocations() {
  const locationSelect = document.getElementById("location");
  locationSelect.innerHTML = '<option value="">Loading states...</option>';

  try {
    const response = await fetch("https://countriesnow.space/api/v0.1/countries/states");
    const result = await response.json();

    if (response.ok && result.data) {
      const us = result.data.find((c) => c.name === "United States");

      if (us && Array.isArray(us.states)) {
        locationSelect.innerHTML = '<option value="">Select your state</option>';

        us.states
          .map((s) => s.name)
          .sort((a, b) => a.localeCompare(b))
          .forEach((state) => {
            const option = document.createElement("option");
            option.value = state;
            option.textContent = state;
            locationSelect.appendChild(option);
          });
      } else {
        locationSelect.innerHTML = '<option value="">Failed to load locations</option>';
      }
    } else {
      locationSelect.innerHTML = '<option value="">Failed to load locations</option>';
    }
  } catch (error) {
    console.error("Error loading locations:", error);
    locationSelect.innerHTML = '<option value="">Error loading locations</option>';
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
    if (existingError) existingError.remove();

    // doesnt work right now, will add the route in the future to actually sign the user up, but for now just redirect to login page
    try {
      const response = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
          location,
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
