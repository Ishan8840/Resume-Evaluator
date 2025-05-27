import "./FileUploader.css";
import { useState, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useDropzone } from 'react-dropzone';


function FileUploader() {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    if (!file) return;
    setFile(file);
  }, [])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    }
  })

  async function handleFileUpload() {
    if (!file) {
      return;
    }
    setStatus("uploading");
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file)
    formData.append('description', description)

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
      setStatus("success");
      setUploadProgress(100);

      navigate("/analyse", {
        state: {
          sections: response.data.sections,
          summary: response.data.summary,
          grammer: response.data.grammer,
          similarity: response.data.similarity
        }
      })

    } catch {
      setStatus("error");
      setUploadProgress(0);
    }
  }

  return (
    <div className="container">
      <h1 className="web-title">Resume Evaluator</h1>

      <div {...getRootProps()}>
        <input {...getInputProps()} />
        {
          isDragActive ?
            <p>Drop the files here ...</p> :
            <p>Drag 'n' drop some files here, or click to select files</p>
        }
      </div>

      {file && (
        <div className="file-info">
          <p>File Name: {file.name}</p>
          <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
          <p>Type: {file.type}</p>
        </div>
      )}

      <div className="description-container">
        <p className="description-title">Enter a job description if you want:</p>
        <input type="text" className="description-input" onChange={(e) => setDescription(e.target.value)} />
      </div>

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



    </div>
  );
}

export default FileUploader;