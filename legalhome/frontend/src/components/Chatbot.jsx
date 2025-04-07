import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [userInput, setUserInput] = useState("");
  const messagesEndRef = useRef(null);
  const [shouldScroll, setShouldScroll] = useState(false);
  const recognition = useRef(null);

  useEffect(() => {
    try {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognition.current = new SpeechRecognition();
        recognition.current.lang = "en-US";
        recognition.current.continuous = false;
        recognition.current.interimResults = false;

        recognition.current.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          setUserInput(transcript);
        };

        recognition.current.onerror = (event) => {
          console.error("Speech recognition error:", event.error);
          addBotMessage("Sorry, I couldn't understand your voice.");
        };
      }
    } catch (error) {
      console.error("Speech recognition not supported:", error);
      addBotMessage("Voice input is not supported in your browser");
    }

    return () => {
      if (recognition.current) recognition.current.abort();
    };
  }, []);

  useEffect(() => {
    if (shouldScroll) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
      setShouldScroll(false);
    }
  }, [shouldScroll]);

  const addBotMessage = (text) => {
    setMessages((prev) => [...prev, { text, sender: "bot" }]);
    setShouldScroll(true);
  };

  const replaceLastBotMessage = (text) => {
    setMessages((prev) => {
      const updated = [...prev];
      const lastIndex = updated.length - 1;
      if (updated[lastIndex].sender === "bot" && updated[lastIndex].text === "Typing...") {
        updated[lastIndex] = { text, sender: "bot" };
      } else {
        updated.push({ text, sender: "bot" });
      }
      return updated;
    });
    setShouldScroll(true);
  };

  const handleStartListening = () => {
    try {
      if (recognition.current) {
        recognition.current.start();
        addBotMessage("Listening...");
      }
    } catch (error) {
      console.error("Error starting speech recognition:", error);
      addBotMessage("Voice input is not supported in your browser");
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const input = userInput.trim();
    if (input) {
      setMessages((prev) => [...prev, { text: input, sender: "user" }]);
      setUserInput(""); // ✅ Clear input immediately
      addBotMessage("Typing..."); // 💬 Typing indicator

      try {
        const response = await axios.post("http://localhost:8000/chatbot/", {
          query: input,
        });

        replaceLastBotMessage(response.data.response || "Sorry, I couldn't understand.");
      } catch (error) {
        console.error("Error fetching response:", error);
        replaceLastBotMessage("There was an error. Please try again.");
      }
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
        <div ref={messagesEndRef} />
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
              type="button"
              className="voice-btn"
              onClick={handleStartListening}
              aria-label="Start voice input"
            >
              <i className="fas fa-microphone"></i>
            </button>
          ) : (
            <button type="submit" className="send-btn" aria-label="Send message">
              <i className="fas fa-paper-plane"></i>
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default Chatbot;
