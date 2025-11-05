// navbar scripts
fetch('components/navbar.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('navbar-placeholder').innerHTML = data;

    setTimeout(() => {
      const hamburger = document.getElementById('hamburger');
      if (hamburger) {
        hamburger.addEventListener('click', function() {
          console.log('Hamburger menu clicked!');
          toggleSidebar();
        });
      }
      const profile = document.getElementById('profileIcon');
      if (profile) {
        profile.addEventListener('click', function() {
          console.log('Profile clicked!');
          // add logic here later (open profile settings)
        });
      }
    }, 0);
  })
  .catch(error => console.error('Error loading navbar:', error));

// can be implemented differently later once we are fetching from db
function updateChatName(newName) {
  const chatNameElement = document.getElementById('chatName');
  if (chatNameElement) {
    chatNameElement.textContent = newName;
  }
}

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');
  if (sidebar && overlay) {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
  }
}

// Example usage:
// setTimeout(() => updateChatName('NEW NAME'), 2000);