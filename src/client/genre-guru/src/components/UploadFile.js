import { FaUpload } from "react-icons/fa";
import "../styles/uploadfile.css";
import { uploadWavFile } from "../services/backend_api";
import { useNavigate } from "react-router-dom";
import React, { useRef } from "react";

const UploadFile = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file || file.type !== "audio/wav") {
      alert("Please upload a valid .wav file.");
      return;
    }

    const reader = new FileReader();
    reader.onload = async () => {
      const base64Wav = reader.result.split(",")[1]; // remove header
      try {
        const deezerTracks = await uploadWavFile(base64Wav);
        navigate("/results", { state: { deezerTracks } });
      } catch (error) {
        console.error("Upload failed (UploadFile.js):", error);
        alert("Error uploading audio file.");
      }
    };
    reader.readAsDataURL(file); // Reads file as base64
  };

  return (
    <div className="upload-wrapper">
      <input
        type="file"
        accept=".wav"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <button className="upload-btn" onClick={() => fileInputRef.current.click()}>
        <FaUpload /> Upload
      </button>
    </div>
  );
};

export default UploadFile;