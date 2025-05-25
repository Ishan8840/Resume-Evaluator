import "./Analysed.css";
import { useState, useEffect } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";


function Analysed() {
  const { state } = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!state) navigate("/");
  }, [state, navigate]);

  if (!state) return null;

  return (
    <>
      <h1>Feedback</h1>
      <h2>Sections</h2>
      <pre>{JSON.stringify(state.sections, null, 2)}</pre>
      <pre>{JSON.stringify(state.summary)}</pre>
    </>
  );
}

export default Analysed;