fetch('components/navbar.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('navbar-placeholder').innerHTML = data;
    const hamburger = document.getElementById('hamburger');
    if (hamburger) {
      hamburger.addEventListener('click', function() {
        console.log('Hamburger menu clicked!');
        // add logic here later (sidebar shown and allows pinning chats)
      });
    }
  })
  .catch(error => console.error('Error loading navbar:', error));

// can be implemented differently later once we are fetching from db
function updateChatName(newName) {
  const chatNameElement = document.getElementById('chatName');
  if (chatNameElement) {
    chatNameElement.textContent = newName;
  }
}

// Example usage:
// setTimeout(() => updateChatName('NEW NAME'), 2000);