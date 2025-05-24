import "./FileUploader.css";
import { useState } from "react";
import axios from "axios";

function FileUploader() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [extractedText, setExtractedText] = useState("");

  function handleFileChange(e) {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  }

  async function handleFileUpload() {
    if (!file) {
      return;
    }
    setStatus("uploading");
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file)

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = progressEvent.total ?
            Math.round((progressEvent.loaded * 100) / progressEvent.total)
            : 0;
          setUploadProgress(progress);
        }
      });

      setExtractedText(response.data.text);

      setStatus("success");
      setUploadProgress(100);
    } catch {
      setStatus("error");
      setUploadProgress(0);
    }
  }

  return (
    <div className="container">
      <h1 className="web-title">Resume Evaluator</h1>

      <input onChange={handleFileChange} type="file" accept=".pdf" className="pdf-input" />

      {file && (
        <div className="file-info">
          <p>File Name: {file.name}</p>
          <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
          <p>Type: {file.type}</p>
        </div>
      )}

      {status === "uploading" && (
        <div className="progress">{uploadProgress}%</div>
      )}

      {file && status != "uploading" &&
        <button className="upload-btn" onClick={handleFileUpload}>Upload</button>
      }

      {file && status === "success" && (
        <p className="success">File Successfully Uploaded!</p>
      )}

      {file && status === "error" && (
        <p className="error">Upload Failed</p>
      )}

      {extractedText && (
        <div>
          <h2>Extracted Text</h2>
          <pre>{extractedText}</pre>
        </div>
      )}

    </div>
  );
}

export default FileUploader;