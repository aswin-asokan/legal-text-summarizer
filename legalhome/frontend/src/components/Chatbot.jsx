import React, { useState } from "react";
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [userInput, setUserInput] = useState("");

  // Define the bot's responses
  const botResponses = {
    "hi": "Hello! How can I assist you?",
    "how are you?": "I'm just a bot, but I'm doing great! How about you?",
    "what is your name?": "I am a chatbot, here to help you!",
    "bye": "Goodbye! Have a great day!",
  };

  // Initialize Speech Recognition API
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = false;

  // Handle speech result
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setUserInput(transcript); // Set the transcribed text to input
  };

  // Handle errors for speech recognition
  recognition.onerror = (event) => {
    console.error("Speech recognition error: ", event.error);
  };

  // Start listening for voice input
  const handleStartListening = () => {
    recognition.start();
    console.log("Microphone is listening...");
  };

  const handleSendMessage = (event) => {
    event.preventDefault();

    const input = userInput.trim().toLowerCase(); // Normalize input

    if (input) {
      const newMessages = [...messages, { text: userInput, sender: "user" }];
      const botReply = botResponses[input] || "Sorry, I didn't understand that."; // Default response
      newMessages.push({ text: botReply, sender: "bot" });

      setMessages(newMessages);
      setUserInput("");
    }
  };

  return (
    <div className="chatbot">
      <div className="header">Chatbot</div>
      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.sender === "bot" ? "bot-message" : "user-message"}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input">
        <form onSubmit={handleSendMessage}>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message..."
          />
          {userInput.trim() === "" ? (
            <button
              className="voice-btn"
              type="button"
              onClick={handleStartListening}
            >
              <i className="fas fa-microphone"></i>
            </button>
          ) : (
            <button className="send-btn" type="submit">
              <i className="fas fa-paper-plane"></i>
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default Chatbot;
