async function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;

    if (!message) return;

    let chatBox = document.getElementById("chat-box");

    // Show user message
    chatBox.innerHTML += `<div class="user">${message}</div>`;

    input.value = "";

    let response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    let data = await response.json();

    // Show bot response
    chatBox.innerHTML += `<div class="bot">${data.response}</div>`;
}