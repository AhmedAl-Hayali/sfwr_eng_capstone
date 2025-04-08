import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/loading.css";
import { getDeezerTrackFromISRC } from "../services/api";
import { fetchRecommendations } from "../services/backend_api";
import { motion } from "framer-motion";

const LoadingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  // const { selectedTrack } = location.state || {};
  // const { deezerTracks } = location.state || {};
  const { selectedTrack, deezerTracks } = location.state || {};

  // Block key input except refresh/system keys
  useEffect(() => {
    const blockKeys = (e) => {
      const allowedKeys = ["F5", "F11", "F12", "Tab"];
      const isCtrlR = (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "r";
      const isAllowed = allowedKeys.includes(e.key) || isCtrlR;

      if (!isAllowed) {
        e.preventDefault();
      }
    };

    window.addEventListener("keydown", blockKeys, true);
    return () => {
      window.removeEventListener("keydown", blockKeys, true);
    };
  }, []);

  // ✅ Recommendation fetch + redirect fallback
  useEffect(() => {
    // Refresh-safe: Redirect to home if no selectedTrack
    if (deezerTracks) {
      // needs to be handled differently as wav gets the trackid's directly
      const getRecommendations = async () => { 
        try {
          //simply set this to deezerTracks I think??
          const recommendedTrackIds = deezerTracks;
          //navigate once we have our ids, but pass empty thing for selectedTrack as we don't have anything there
          console.log("Recommended Track IDs:", recommendedTrackIds);
          navigate("/results", {
            state: { trackIds: recommendedTrackIds, selectedTrack: null },
          });
        } catch (err) {
          console.error("Error fetching recommendations:", err);
          alert("Error getting recommendations.");
          navigate("/");
        }
      };
      getRecommendations();
      return; // Stop further execution in this effect.
    }

    if (!selectedTrack || !selectedTrack.external_ids?.isrc) {
      console.warn("No selectedTrack found. Probably a refresh on /loading.");
      navigate("/", { replace: true });
      return;
    }

    const getAndSendRecommendations = async () => {
      try {
        const isrc = selectedTrack.external_ids.isrc;
        console.log("ISRC:", isrc);

        const deezerTrack = await getDeezerTrackFromISRC(isrc);
        console.log("Deezer Track:", deezerTrack);

        if (!deezerTrack) throw new Error("Could not fetch Deezer track");

        const recommendedTrackIds = await fetchRecommendations(deezerTrack);
        console.log("Recommended Track IDs:", recommendedTrackIds);

        navigate("/results", {
          state: { trackIds: recommendedTrackIds, selectedTrack },
        });
      } catch (err) {
        console.error("Error fetching recommendations:", err);
        alert("Error getting recommendations.");
        navigate("/");
      }
    };

    getAndSendRecommendations();
  }, [selectedTrack, deezerTracks, navigate]);

  return (
    <motion.div
      className="loading-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* 🛡️ Input blocker */}
      <div className="input-blocker"></div>

      <div className="spinner"></div>
      <p>Getting your recommendations...</p>
    </motion.div>
  );
};

export default LoadingPage;
