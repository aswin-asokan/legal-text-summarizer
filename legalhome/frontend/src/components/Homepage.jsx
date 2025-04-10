import React, { useState } from "react";
import axios from "axios";
import { FaCommentDots } from "react-icons/fa";
import "./Homepage.css";

const Homepage = () => {
  const [file, setFile] = useState(null);
  const [textContent, setTextContent] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

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

    setLoading(true);
    setTextContent(""); // Clear previous content when new upload starts

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
      setLoading(false);
    }
  };

  const scrollToChatbot = () => {
    const chatbotSection = document.getElementById("chatbot");
    if (chatbotSection) {
      chatbotSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="homepage" style={{ textAlign: "center", marginTop: "50px", position: "relative", minHeight: "100vh" }}>
      {/* Floating Chatbot Icon - Only visible when there's no text content */}
      {!textContent && (
        <button 
          className="chatButton"
          onClick={scrollToChatbot}
          onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.1)")}
          onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
        >
          <FaCommentDots style={{ color: "white", fontSize: "28px" }} />
        </button>
      )}

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

      { textContent && !loading && (
  <div
    style={{
      margin: "20px auto",
      textAlign: "justify",
      padding: "20px",
      border: "1px solid #ddd",
      borderRadius: "5px",
      backgroundColor: "#fff",
    }}
  >
    <h2>Summary:</h2>
    <p dangerouslySetInnerHTML={{ __html: textContent.replace(/\n/g, "<br />") }} />
  </div>
)}

    </div>
  );
};

export default Homepage;