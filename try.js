async function sendMessage() {
    const prompt = document.getElementById("prompt").value;
    const chatContainer = document.getElementById("chat-container");

    if (!prompt) {
        alert("Please enter a message.");
        return;
    }

    // Add user message to chat
    const userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerHTML = `
        <div class="message-avatar" style="background-color: #1877f2;"></div>
        <div class="message-content">${prompt}</div>
    `;
    chatContainer.appendChild(userMessage);

    // Send the prompt to the Flask backend
    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt }),
        });

        if (response.ok) {
            const data = await response.json();
            const aiMessage = document.createElement("div");
            aiMessage.className = "message ai-message";
            aiMessage.innerHTML = `
                <div class="message-avatar" style="background-color: #e8e8e8;"></div>
                <div class="message-content">${data.generated_text[0]}</div>
            `;
            chatContainer.appendChild(aiMessage);
        } else {
            const errorData = await response.json();
            alert("Error: " + (errorData.error || "Unable to generate response."));
        }
    } catch (error) {
        alert("Error: Unable to connect to the server.");
    }

    // Clear the input field
    document.getElementById("prompt").value = "";

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}