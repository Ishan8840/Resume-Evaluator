from flask import Flask, jsonify, request
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:5173"])


@app.route("/upload", methods=["POST", "GET"])
def upload():
  if "file" not in request.files:
    return {"error": "No file part"}, 400
  
  file = request.files['file']

  if file.filename == "":
    return {"error": "No selected file"}, 400

  with pdfplumber.open(file) as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""

  return {"message": "File uploaded successfully", "text": text}


if __name__ == "__main__":
  app.run(debug=True)