from flask import Flask, jsonify, request
from flask_cors import CORS
import pdfplumber
import re

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:5173"])


def section_extraction(text):
    required_sections = {
        "Experience": ["experience", "work experience", "professional experience"],
        "Education": ["education", "academic background"],
        "Skills": ["skills", "technical skills"],
        "Contact": ["Contact", "Email"],
        "Objective": ["Objective", "Summary"],
    }
    found_sections = {}

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"\b(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){1,2}\d{4}\b"
    linkedin_pattern = r"https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+"

    found_email = bool(re.search(email_pattern, text))
    found_phone = bool(re.search(phone_pattern, text))
    found_linkedin = bool(re.search(linkedin_pattern, text))

    for section, keywords in required_sections.items():
        found_sections[section] = any(
            re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in keywords
        )

    found_sections["Contact"] = found_email or found_phone or found_linkedin

    return found_sections


def section_summary(sections):
    missing_sections = [key for key, value in sections.items() if not value]
    if not missing_sections:
        return "Your resume includes all key sections."
    else:
        sections_list = ", ".join(missing_sections)
        return f"Consider adding a section for {sections_list}."


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "No selected file"}, 400

    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text(x_tolerance=2, y_tolerance=2) or ""

    section_check = section_extraction(text)

    summary = section_summary(section_check)

    return {"text": text, "sections": section_check, "summary": summary}


if __name__ == "__main__":
    app.run(debug=True)
