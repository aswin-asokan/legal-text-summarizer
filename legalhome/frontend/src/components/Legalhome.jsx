import React, { useState } from "react";
import "./Legalhome.css";
import LegalImage from "../assets/court.jpg"; // Import your image
import LegalImage1 from "../assets/court1.jpg"; // Import your image


const Home = () => {
  const [flipped, setFlipped] = useState(false);

    // Function to scroll to the Chatbot section
    const scrollToSummary = () => {
        const summarySection = document.getElementById("homepage");
        console.log("Summary Section:", summarySection); // Debugging: Log the element
        if (summarySection) {
          summarySection.scrollIntoView({ behavior: "smooth" });
        }
      };
  return (
    <div className="home-container">
      {/* Hero Section */}
      <div className="hero">
        {/* Left Side: Text */}
        <div className="hero-text">
          <h1>AI-Powered Legal Text Summarizer</h1>
          <p>
            Simplify complex legal documents with our AI-driven summarizer. Save time, enhance comprehension, and get key insights in seconds.
          </p>
          <button className="cta-button" onClick={scrollToSummary}  >Summarize Now</button>
        </div>

        {/* Right Side: Image */}
        <div className="hero-image" onClick={() => setFlipped(!flipped)}>
            <div className={`flip-container ${flipped ? "flipped" : ""}`}>
                {/* Front Side */}
                <div className="front">
                    <img src={LegalImage} alt="Legal Concept Front" />
                </div>
                {/* Back Side */}
                <div className="back">
                    <img src={LegalImage1} alt="Legal Concept Back" />
                </div>
            </div>
        </div>

      </div>

      {/* Features Section */}
      <div className="features">
        <div className="feature-item">
          <h2>📜 Understand Legal Texts Faster</h2>
          <p>Convert lengthy legal documents into concise, easy-to-read summaries.</p>
        </div>
        <div className="feature-item">
          <h2>⚖️ Accurate & AI-Powered</h2>
          <p>Our AI ensures that key legal terms and concepts are preserved.</p>
        </div>
        <div className="feature-item">
          <h2>🔍 Find Key Information Instantly</h2>
          <p>No more scrolling through pages—get the essential points in seconds.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
