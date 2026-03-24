// signup scripts

const formSteps = document.querySelectorAll(".form-step");
const progressBar = document.getElementById("progress-bar");
const stepCounter = document.getElementById("step-counter");
const stepTitle = document.getElementById("step-title");
const signupForm = document.getElementById("signup-form");
let currentStep = 0;

let cropper;
const imageInput = document.getElementById("profile-pic");
const uploadTrigger = document.getElementById("upload-trigger");
const cropperModal = document.getElementById("cropper-modal");
const cropperImage = document.getElementById("cropper-image");
const profilePreview = document.getElementById("profile-preview");
const saveCropBtn = document.getElementById("save-crop");
const cancelCropBtn = document.getElementById("cancel-crop");
let croppedImageDataUrl = null;

const stepTitles = [
  "Create Your Account",
  "Tell Us About Yourself",
  "Finish Your Profile",
];

uploadTrigger.addEventListener("click", () => imageInput.click());

imageInput.addEventListener("change", (e) => {
  const files = e.target.files;
  if (files && files.length > 0) {
    const reader = new FileReader();
    reader.onload = (event) => {
      cropperImage.src = event.target.result;
      cropperModal.style.display = "flex";

      if (cropper) cropper.destroy();
      cropper = new Cropper(cropperImage, {
        aspectRatio: 1,
        viewMode: 1,
        background: false,
      });
    };
    reader.readAsDataURL(files[0]);
  }
});

saveCropBtn.addEventListener("click", () => {
  const canvas = cropper.getCroppedCanvas({
    width: 300,
    height: 300,
  });

  croppedImageDataUrl = canvas.toDataURL("image/jpeg");
  profilePreview.src = croppedImageDataUrl;
  cropperModal.style.display = "none";
  cropper.destroy();
});

cancelCropBtn.addEventListener("click", () => {
  cropperModal.style.display = "none";
  if (cropper) cropper.destroy();
  imageInput.value = "";
});


function updateFormSteps() {
  formSteps.forEach((step, index) => {
    step.classList.toggle("form-step-active", index === currentStep);
  });

  const progress = (currentStep / (formSteps.length - 1)) * 100;
  progressBar.style.width = progress + "%";

  const stepNumber = currentStep + 1;
  const totalSteps = formSteps.length;

  stepCounter.textContent = `Step ${stepNumber} out of ${totalSteps}`;
  stepTitle.textContent = stepTitles[currentStep];
}

document.querySelectorAll("#signup-form .btn-next").forEach((button) => {
  button.addEventListener("click", () => {
    const inputs = formSteps[currentStep].querySelectorAll("input, select");
    let isValid = true;

    inputs.forEach((input) => {
      if (!input.checkValidity()) {
        input.reportValidity();
        isValid = false;
      }
    });

    if (currentStep === 0) {
      const password = document.getElementById("password").value;
      const confirm = document.getElementById("confirm-password").value;
      if (password !== confirm) {
        showError("Passwords do not match!");
        isValid = false;
      }
    }

    if (isValid) {
      currentStep++;
      updateFormSteps();
    }
  });
});

document.querySelectorAll("#signup-form .btn-prev").forEach((button) => {
  button.addEventListener("click", () => {
    currentStep--;
    updateFormSteps();
  });
});

async function loadLocations() {
  const locationSelect = document.getElementById("location");
  if (!locationSelect) return;

  locationSelect.innerHTML = '<option value="">Loading states...</option>';

  try {
    const response = await fetch(
      "https://countriesnow.space/api/v0.1/countries/states",
    );
    const result = await response.json();

    if (response.ok && result.data) {
      const us = result.data.find((c) => c.name === "United States");

      if (us && Array.isArray(us.states)) {
        locationSelect.innerHTML =
          '<option value="">Select your state</option>';
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
        locationSelect.innerHTML =
          '<option value="">Failed to load locations</option>';
      }
    } else {
      locationSelect.innerHTML =
        '<option value="">Failed to load locations</option>';
    }
  } catch (error) {
    console.error("Error loading locations:", error);
    locationSelect.innerHTML =
      '<option value="">Error loading locations</option>';
  }
}

signupForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const submitButton = document.getElementById("submit-btn");
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const location = document.getElementById("location").value;

  submitButton.disabled = true;
  submitButton.textContent = "Signing up...";

  const existingError = document.querySelector(".error-message");
  if (existingError) existingError.remove();

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
        profile_picture: croppedImageDataUrl,
      }),
      credentials: "include",
    });

    const data = await response.json();

    if (response.ok && data.success) {
      window.location.href = "/login";
    } else {
      showError(data.message || "Signup failed. Please try again.");
      submitButton.disabled = false;
      submitButton.textContent = "Complete Sign Up";
    }
  } catch (error) {
    console.error("Signup error:", error);
    showError("An error occurred. Please try again.");
    submitButton.disabled = false;
    submitButton.textContent = "Complete Sign Up";
  }
});

function showError(message) {
  const existingError = document.querySelector(".error-message");
  if (existingError) existingError.remove();

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
  signupForm.reset();
  loadLocations();
  updateFormSteps();
});
