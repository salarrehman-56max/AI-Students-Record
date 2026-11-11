import os

from groq import Groq


def _ask_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Groq API key not found. Add GROQ_API_KEY to your .env file.")

    model = os.getenv("GROQ_MODEL", "").strip() or "llama-3.3-70b-versatile"
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful academic mentor. Give clear, supportive, practical advice."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=700,
    )
    return response.choices[0].message.content.strip()


def _student_summary(student):
    subjects = student.get("subjects", [])
    marks = student.get("marks", [])
    results = ", ".join(
        f"{subject}: {mark}/100"
        for subject, mark in zip(subjects, marks)
    )
    return (
        f"Student: {student.get('name', 'Student')}\n"
        f"Class/Semester: {student.get('class_semester', 'N/A')}\n"
        f"Subject marks: {results}\n"
        f"Average: {student.get('average', 'N/A')}%\n"
        f"Grade: {student.get('grade', 'N/A')}"
    )


def analyze_performance(student):
    prompt = (
        "Analyze this student's academic performance. Identify strong subjects, "
        "subjects needing improvement, and give 3-5 specific suggestions. "
        "Be encouraging and avoid making assumptions beyond the marks.\n\n"
        + _student_summary(student)
    )
    return _ask_groq(prompt)


def generate_study_tips(student):
    prompt = (
        "Create a simple, realistic weekly study plan and practical study tips "
        "based on this student's subject marks. Prioritize weaker subjects, "
        "include short study sessions and revision, and keep the tone encouraging.\n\n"
        + _student_summary(student)
    )
    return _ask_groq(prompt)
