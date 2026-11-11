# AI Student Record Manager

A beginner-friendly Flask application for managing student records, calculating results, and generating AI-powered academic feedback using Groq.

## Requirements
- Windows
- Python 3
- VS Code
- A Groq API key for AI features

## Setup (Windows PowerShell)
1. Open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
4. Activate it:
   ```powershell
   venv\Scripts\Activate
   ```
   If PowerShell blocks activation, use Command Prompt and run `venv\Scripts\activate.bat`.
5. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env` and add your Groq key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key
   GROQ_MODEL=
   ```
   Keep `.env` private. Never upload it or share screenshots containing the key.
7. Start the app:
   ```powershell
   python app.py
   ```
8. Open http://127.0.0.1:5000 in Chrome.

## Features
- Add, view, search, update, and delete students
- Subject marks validation
- Automatic total, average, and grade calculation
- AI performance analysis and study tips
- Local JSON storage in `students.json`

## Grade rules
- A: 85% or above
- B: 70% to below 85%
- C: 60% to below 70%
- D: 50% to below 60%
- F: below 50%

AI features require internet access and a valid Groq API key. Record management and calculations work without the AI service.

## Stop the app
Press `Ctrl+C` in the terminal running Flask.
