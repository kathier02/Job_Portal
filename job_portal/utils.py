import re
import PyPDF2

SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "api", "data analysis", "sql", "nosql", "aws", "azure",
    "docker", "kubernetes", "linux", "git", "rest",
    "django", "flask", "html", "css", "javascript"
]



def extract_text_from_pdf(pdf_file):

    text = ""

    try:
        pdf_stream = io.BytesIO(pdf_file.read())
        reader = PyPDF2.PdfReader(pdf_stream)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    except Exception as e:
        print("PDF ERROR:", e)
        return ""

    return text.lower()


def clean_text(text):
    if text is None:
        return ""

    return re.sub(
        r"[^a-z0-9+\s]",
        " ",
        str(text).lower()
    )


def skill_present(skill, text):
    skill = skill.strip().lower()
    text = text.lower()

    if " " in skill:
        return skill in text

    return skill in text.split()


def find_missing_skills(resume_text, job_text):
    missing = []

    for skill in SKILLS:
        job_has_skill = skill_present(skill, job_text)
        resume_has_skill = skill_present(skill, resume_text)


        if job_has_skill and not resume_has_skill:
            missing.append(skill)

    return missing
