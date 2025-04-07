import React from "react";
import Chatbot from "./components/Chatbot";
import Homepage from "./components/Homepage";
import Home from "./components/Legalhome";
import "./App.css";

function App() {
  return (
    <div className="App">
      {/* Homepage Section */}
      <section id ="home" className="page">
        <Home />
      </section>
      {/* Homepage Section */}
      <section id ="homepage" className="page">
        <Homepage />
      </section>

      {/* Chatbot Section */}
      <section id ="chatbot" className="page">
        <Chatbot />
      </section>
    </div>
  );
}

export default App;