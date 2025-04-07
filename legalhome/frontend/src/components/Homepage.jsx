import React, { useState } from "react";
import axios from "axios";
import { FaCommentDots } from "react-icons/fa";
import "./Homepage.css";

const Homepage = () => {
  const [file, setFile] = useState(null);
  const [textContent, setTextContent] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // New state for loading

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError("");
    } else {
      setError("Please upload a valid PDF file.");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      setError("");
    } else {
      setError("Please upload a valid PDF file.");
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    setLoading(true); // Show loading state

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setTextContent(response.data.text || "No text extracted.");
      setError("");
    } catch (err) {
      setError("Failed to convert PDF to text. Please try again.");
      setTextContent("");
    } finally {
      setLoading(false); // Hide loading button after request completes
    }
  };

  // Function to scroll to the Chatbot section
  const scrollToChatbot = () => {
    const chatbotSection = document.getElementById("chatbot");
    if (chatbotSection) {
      chatbotSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="homepage" style={{ textAlign: "center", marginTop: "50px", position: "relative", minHeight: "100vh" }}>
      {/* Floating Chatbot Icon - Scroll to Chatbot Section */}
      <button
        onClick={scrollToChatbot}
        style={{
          position: "absolute",
          bottom: "57px",
          right: "30px",
          zIndex: 1000,
          backgroundColor: "#00aaa5",
          borderRadius: "50%",
          padding: "15px",
          boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          transition: "transform 0.3s ease",
          border: "none",
        }}
        onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.1)")}
        onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
      >
        <FaCommentDots style={{ color: "white", fontSize: "28px" }} />
      </button>

      {/* PDF to Text Converter Content */}
      <h1>Legal Text Summarizer</h1>
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        style={{
          border: "2px dashed #007bff",
          borderRadius: "10px",
          padding: "20px",
          margin: "20px auto",
          maxWidth: "400px",
          backgroundColor: "#f9f9f9",
        }}
      >
        <p>Drag & Drop a PDF file here</p>
        <input
          type="file"
          id="file-input"
          accept="application/pdf"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
        <label
          htmlFor="file-input"
          style={{
            display: "inline-block",
            padding: "10px 20px",
            backgroundColor: "#007bff",
            color: "white",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Choose File
        </label>
      </div>

      {file && <p>Selected file: {file.name}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Upload Button with Loading Effect */}
      <button
        onClick={handleUpload}
        disabled={loading}
        style={{
          padding: "10px 20px",
          backgroundColor: loading ? "#ccc" : "#28a745",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          marginTop: "20px",
        }}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {/* Show Extracted Text After Loading Completes */}
      {textContent && !loading && (
        <div
          style={{
            margin: "20px auto",
            textAlign: "justify",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            backgroundColor: "#fff",
          }}
        >
          <h2>Summary :</h2>
          <p>{textContent.split("\n").map((line, index) => (
  <React.Fragment key={index}>
    {line}
    <br />
  </React.Fragment>
))}</p>

        </div>
      )}
    </div>
  );
};

export default Homepage;
