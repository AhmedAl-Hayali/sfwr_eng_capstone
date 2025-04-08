import { FaUpload } from "react-icons/fa";
import "../styles/uploadfile.css";
import { uploadWavFile } from "../services/backend_api";
import { useNavigate } from "react-router-dom";
import React, { useRef, useState } from "react";

const UploadFile = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file || file.type !== "audio/wav") {
      alert("Please upload a valid .wav file.");
      return;
    }
    try {
      setUploading(true);
      // Create a new FileReader instance
      const reader = new FileReader();
  
      // Wrap the file reading in a Promise so we can await its completion
      const base64Data = await new Promise((resolve, reject) => {
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(new Error("Error reading file."));
        reader.readAsDataURL(file);
      });

      console.log("reached here");
  
      // Remove the header so that only the base64 part remains
      const base64Wav = base64Data.split(",")[1];
      
      console.log("successfully read to base64wav");
      // wait for a response from the server
      const deezerTracks = await uploadWavFile(base64Wav);
      
      console.log("received results...navigating");
      // Navigate to the results page with the returned tracks
      navigate("/results", { state: { deezerTracks } });
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Error uploading audio file.");
    } finally {
      setUploading(false);
    }
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
      <button className="upload-btn" onClick={() => fileInputRef.current.click()} disabled={uploading}>
        {uploading ? "Uploading..." : <><FaUpload /> Upload</>}
      </button>
    </div>
  );
};

export default UploadFile;