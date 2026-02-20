import pdfplumber
import re


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content
    return text


def extract_name(text):
    lines = text.split("\n")

    blacklist = [
        "resume", "objective", "summary",
        "skills", "education", "experience", "profile"
    ]

    for line in lines[:10]:
        clean = line.strip()

        if len(clean.split()) <= 4:
            if not any(word in clean.lower() for word in blacklist):
                if re.match(r'^[A-Z][a-zA-Z.\s]+$', clean):
                    return clean

    return "Name Not Found"


def extract_skills(text):

    skill_list = [
        "python", "java", "c", "c++",
        "html", "css", "javascript",
        "react", "angular", "vue",
        "flask", "django", "api",
        "sql", "mysql", "postgresql",
        "machine learning", "tensorflow",
        "pandas", "numpy", "scikit-learn",
        "data analysis", "excel",
        "power bi", "tableau"
    ]

    found = []
    lower_text = text.lower()

    for skill in skill_list:
        if skill in lower_text:
            found.append(skill)

    return found


def suggest_best_role(user_skills):

    role_database = {

        "Backend Developer": [
            "python", "java", "flask", "django", "sql", "api"
        ],

        "Frontend Developer": [
            "html", "css", "javascript", "react", "angular"
        ],

        "Machine Learning Engineer": [
            "python", "machine learning",
            "pandas", "numpy", "tensorflow"
        ],

        "Full Stack Developer": [
            "html", "css", "javascript",
            "react", "flask", "sql"
        ],

        "Data Analyst": [
            "python", "sql",
            "excel", "power bi", "tableau"
        ]
    }

    results = []

    for role, required_skills in role_database.items():

        matched = [s for s in required_skills if s in user_skills]
        missing = [s for s in required_skills if s not in user_skills]

        score = int((len(matched) / len(required_skills)) * 100)

        results.append({
            "role": role,
            "score": score,
            "matched": matched,
            "missing": missing
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results