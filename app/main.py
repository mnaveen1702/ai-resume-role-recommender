from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.extractor import (
    extract_text_from_pdf,
    extract_name,
    extract_skills,
    suggest_best_role
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):

    text = extract_text_from_pdf(file.file)
    name = extract_name(text)
    resume_skills = extract_skills(text)

    role_results = suggest_best_role(resume_skills)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "name": name,
            "resume_skills": resume_skills,
            "role_results": role_results
        }
    )