import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "".join([page.get_text() for page in doc])

def extract_candidate_data(text, jd_keywords):
    name = re.findall(r"(?i)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    email = re.findall(r"\S+@\S+", text)
    phone = re.findall(r"\+?\d[\d -]{8,}\d", text)

    words = set(re.sub(r"[^\w\s]", "", text.lower()).split())
    matched = words & jd_keywords

    experience = 0
    exp_match = re.search(r"(\d+)\s+years", text.lower())
    if exp_match:
        experience = int(exp_match.group(1))

    return {
        "name": name[0] if name else "Unknown",
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found",
        "matched_keywords": ", ".join(matched),
        "experience": experience,
        "full_resume": text
    }
