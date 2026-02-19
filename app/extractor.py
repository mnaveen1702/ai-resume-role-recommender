import re
import PyPDF2


# -------------------------
# PDF TEXT EXTRACTION
# -------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()


# -------------------------
# NAME EXTRACTION
# -------------------------
def extract_name(text):
    lines = text.split("\n")

    ignore_words = [
        "objective", "summary", "education",
        "skills", "projects", "experience",
        "profile", "career", "about"
    ]

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip headings
        if line.lower() in ignore_words:
            continue

        # Name usually 2-4 words
        words = line.split()

        if 1 < len(words) <= 4:
            # Check if mostly alphabets
            if all(word.isalpha() for word in words):
                return line.title()

    return "Name Not Found"



# -------------------------
# SKILL EXTRACTION
# -------------------------
def extract_skills(text):

    skills_db = [
        "python", "java", "c", "c++", "sql",
        "react", "javascript", "html", "css",
        "machine learning", "data structures",
        "oop", "git", "github", "firebase",
        "rest api"
    ]

    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# -------------------------
# ROLE SUGGESTION ENGINE
# -------------------------
def suggest_best_role(skills):

    role_map = {
        "Frontend Developer": ["react", "javascript", "html", "css"],
        "Backend Developer": ["python", "java", "sql", "rest api"],
        "Machine Learning Engineer": ["python", "machine learning"],
        "Full Stack Developer": ["react", "python", "sql", "javascript"]
    }

    best_role = "No Matching Role"
    best_score = 0

    for role, role_skills in role_map.items():

        match_count = len(set(skills) & set(role_skills))

        if len(skills) == 0:
            score = 0
        else:
            # Hybrid Smart Formula 🔥
            score = int(
                (match_count / len(role_skills)) * 70 +
                (match_count / len(skills)) * 30
            )

        if score > best_score:
            best_score = score
            best_role = role

    # Suitability Message Logic
    if best_score >= 80:
        message = "Highly Suitable for this Role 🚀"
    elif best_score >= 60:
        message = "Good Match 👍"
    else:
        message = "Needs Skill Improvement 📚"

    return best_role, best_score, message
