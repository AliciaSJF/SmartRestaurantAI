document.getElementById("send-button").addEventListener("click", async function () {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const question = userInput.value;
    if (!question) {
        alert("Por favor, escribe una pregunta.");
        return;
    }

    // Mostrar la pregunta del usuario en el chat
    const userMessage = document.createElement("div");
    userMessage.classList.add("user-message");
    userMessage.textContent = `Tú: ${question}`;
    chatBox.appendChild(userMessage);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (response.ok) {
            const data = await response.json();

            // Mostrar la respuesta del chatbot en el chat
            const botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");
            botMessage.textContent = `Bot: ${data.response}`;
            chatBox.appendChild(botMessage);
        } else {
            throw new Error("Error al obtener respuesta del servidor.");
        }
    } catch (error) {
        console.error("Error:", error);
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("bot-message");
        errorMessage.textContent = "Bot: Lo siento, hubo un error.";
        chatBox.appendChild(errorMessage);
    }

    userInput.value = ""; // Limpiar el campo de entrada
    chatBox.scrollTop = chatBox.scrollHeight; // Hacer scroll hacia abajo
});