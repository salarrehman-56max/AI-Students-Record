import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ai_helper import analyze_performance, generate_study_tips

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "students.json"

load_dotenv(BASE_DIR / ".env")
app = Flask(__name__)


def load_students():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=2, ensure_ascii=False)


def calculate_result(marks):
    total = sum(marks)
    average = total / len(marks) if marks else 0
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
    return total, round(average, 2), grade


def validate_student(payload):
    student_id = str(payload.get("student_id", "")).strip()
    name = str(payload.get("name", "")).strip()
    class_semester = str(payload.get("class_semester", "")).strip()
    subjects = payload.get("subjects", [])
    marks = payload.get("marks", [])

    if not student_id or not name or not class_semester:
        raise ValueError("Student ID, name, and class/semester are required.")
    if not isinstance(subjects, list) or not isinstance(marks, list) or not subjects:
        raise ValueError("Enter at least one subject and its marks.")
    if len(subjects) != len(marks):
        raise ValueError("Each subject must have one matching mark.")

    clean_subjects, clean_marks = [], []
    for subject, mark in zip(subjects, marks):
        subject = str(subject).strip()
        if not subject:
            raise ValueError("Subject names cannot be empty.")
        try:
            mark = float(mark)
        except (TypeError, ValueError):
            raise ValueError("Marks must be numbers.")
        if mark < 0 or mark > 100:
            raise ValueError("Marks must be between 0 and 100.")
        clean_subjects.append(subject)
        clean_marks.append(round(mark, 2))

    total, average, grade = calculate_result(clean_marks)
    return {
        "student_id": student_id,
        "name": name,
        "class_semester": class_semester,
        "subjects": clean_subjects,
        "marks": clean_marks,
        "total": round(total, 2),
        "average": average,
        "grade": grade,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/students")
def get_students():
    return jsonify(load_students())


@app.post("/api/students")
def add_student():
    try:
        student = validate_student(request.get_json(force=True))
        students = load_students()
        if any(s["student_id"].lower() == student["student_id"].lower() for s in students):
            return jsonify({"error": "A student with this ID already exists."}), 409
        students.append(student)
        save_students(students)
        return jsonify(student), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.put("/api/students/<student_id>")
def update_student(student_id):
    try:
        student = validate_student(request.get_json(force=True))
        if student["student_id"] != student_id:
            return jsonify({"error": "Student ID cannot be changed."}), 400
        students = load_students()
        for index, existing in enumerate(students):
            if existing["student_id"].lower() == student_id.lower():
                students[index] = student
                save_students(students)
                return jsonify(student)
        return jsonify({"error": "Student not found."}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.delete("/api/students/<student_id>")
def delete_student(student_id):
    students = load_students()
    updated = [s for s in students if s["student_id"].lower() != student_id.lower()]
    if len(updated) == len(students):
        return jsonify({"error": "Student not found."}), 404
    save_students(updated)
    return jsonify({"message": "Student deleted."})


@app.post("/api/ai/analyze")
def ai_analyze():
    payload = request.get_json(force=True)
    try:
        result = analyze_performance(payload.get("student", {}))
        return jsonify({"result": result})
    except Exception as error:
        return jsonify({"error": str(error)}), 502


@app.post("/api/ai/study-tips")
def ai_study_tips():
    payload = request.get_json(force=True)
    try:
        result = generate_study_tips(payload.get("student", {}))
        return jsonify({"result": result})
    except Exception as error:
        return jsonify({"error": str(error)}), 502


if __name__ == "__main__":
    print("AI Student Record Manager is running!")
    print("Open this link in Chrome: http://127.0.0.1:5000")
    print("(Press Ctrl+C in this terminal to stop the app)")
    app.run(host="127.0.0.1", port=5000, debug=False)
