import { useState, useEffect } from 'react';
import './App.css';
import FileUploader from './Components/FileUploader';
import Analysed from './Components/Analysed';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={<FileUploader />} />
          <Route path='/analyse' element={<Analysed />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
