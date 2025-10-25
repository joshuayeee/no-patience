fetch("components/chat.html")
  .then((response) => response.text())
  .then((data) => {
    document.getElementById("chat-container").innerHTML = data;

    setTimeout(() => {
      const sendButton = document.getElementById("sendButton");
      const chatInput = document.getElementById("chatInput");
      const chatMessages = document.getElementById("chatMessages");

      function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
          console.log("Sending message:", message);

          const messageWrapper = document.createElement("div");
          messageWrapper.className = "message-wrapper message-right";

          messageWrapper.innerHTML = `
      <div class="message-container">
        <div class="message-content">
          <p class="message-text">${message}</p>
          <span class="message-time time-right">${new Date().toLocaleTimeString(
            "en-US",
            {
              hour: "2-digit",
              minute: "2-digit",
            }
          )}</span>
        </div>
      </div>
    `;

          chatMessages.appendChild(messageWrapper);

          chatInput.value = "";

          chatMessages.scrollTop = chatMessages.scrollHeight;
        }
      }

      if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
      }

      if (chatInput) {
        chatInput.addEventListener("keypress", function (e) {
          if (e.key === "Enter") {
            sendMessage();
          }
        });
      }
    }, 0);
  })
  .catch((error) => console.error("Error loading chat:", error));

// Can be implemented differently later once we are fetching from db
function updateChatName(newName) {
  const chatNameElement = document.getElementById("chatName");
  if (chatNameElement) {
    chatNameElement.textContent = newName;
  }
}

// Example usage:
// updateChatName("Babiker's Chat");
