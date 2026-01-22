// sidebar scripts
fetch('/sidebar')// + Date.now())
  .then(response => response.text())
  .then(data => {
    console.log('Sidebar HTML loaded:', data.length, 'characters');
    document.getElementById('sidebar-placeholder').innerHTML = data;
    
    setTimeout(() => {
      const chatItems = document.querySelectorAll('.chat-item');
      console.log('Found', chatItems.length, 'chat items');
      
      const overlay = document.getElementById('sidebarOverlay');
      if (overlay) {
        overlay.addEventListener('click', function() {
          toggleSidebar();
        });
      }

      const newChatBtn = document.getElementById('newChatBtn');
      if (newChatBtn) {
        newChatBtn.addEventListener('click', function() {
          console.log('New chat clicked!');
        });
      }

      chatItems.forEach(item => {
        item.addEventListener('click', function() {
          chatItems.forEach(i => i.classList.remove('active'));
          this.classList.add('active');
          
          const chatName = this.querySelector('span').textContent;
          updateChatName(chatName);
          
          console.log('Chat selected:', chatName);
        });
      });
    }, 0);
  })
  .catch(error => console.error('Error loading sidebar:', error));