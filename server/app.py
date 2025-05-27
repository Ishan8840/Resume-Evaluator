from flask import Flask, jsonify, request
from flask_cors import CORS
import pdfplumber
import re
import language_tool_python
from sentence_transformers import SentenceTransformer, util

tool = language_tool_python.LanguageTool("en-US")
model = SentenceTransformer("all-MiniLM-L6-v2")


app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:5173"])


def similarity_check(text, description):
    sentences = [
        text,
        description,
    ]

    embeddings = model.encode(sentences)

    similarities = util.cos_sim(embeddings, embeddings)
    score = float(similarities[0][1])
    score_percent = score * 100

    score_formatted = "{:.2f}".format(score_percent)

    if score_percent < 30:
        similarity_summary = f"Your resume does not match with the job descirption very well. {score_formatted}% match"
    elif score_percent < 60:
        similarity_summary = f"Your resume has some key points from the job description. Consider adding some keywords. {score_formatted}% match"
    else:
        similarity_summary = f"Your resume is a good match. {score_formatted}% match"

    return similarity_summary


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


def grammer_check(text):
    matches = tool.check(text)
    if matches:
        return "There are some grammar and spelling errors on your resume!"
    else:
        return "Your grammar and resume are perfect!"


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]
    description = request.form.get("description", "").strip()

    if file.filename == "":
        return {"error": "No selected file"}, 400

    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text(x_tolerance=2, y_tolerance=2) or ""

    section_check = section_extraction(text)
    summary = section_summary(section_check)
    grammer = grammer_check(text)
    if description:
        similarity = similarity_check(text, description)

    return {
        "sections": section_check,
        "summary": summary,
        "grammer": grammer,
        "similarity": similarity,
    }


if __name__ == "__main__":
    app.run(debug=True)
