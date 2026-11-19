# Online Examination and Result Management System
### Presidency University — School of Computer Science & Engineering
**B.Tech CSE Course:** CSE2271 – Mini Project Review & Demo  
**Architecture:** 3-Tier Model-View-Controller (MVC)  
**Technology Stack:** HTML5, CSS3, Vanilla JavaScript (ES6+), Python Flask, SQLite, Flask-SQLAlchemy

---

## 📌 Executive Summary

The **Online Examination and Result Management System** is a full-stack, secure, proctored web application engineered for university academic departments to conduct paperless assessments, eliminate grading latency, enforce academic integrity via client-side proctoring telemetry, and deliver instantaneous candidate scorecards with topic-by-topic analytics.

- **Frontend:** Semantic HTML5, CSS3 Grid/Flexbox, Vanilla JavaScript (ES6+). Zero third-party frontend frameworks (No React, Angular, or Node.js).
- **Backend:** Python Flask (v3.1.3) utilizing lightweight MVC controller routes and session management.
- **Database & ORM:** SQLite 3 with Flask-SQLAlchemy ORM (ACID transactional guarantees).
- **Security:** Salted password hashing via Werkzeug Security (`generate_password_hash`, `check_password_hash`), cryptographically signed session cookies, and zero answer key exposure in client payloads.
- **Proctoring:** HTML5 Fullscreen lockdown and Page Visibility API (`visibilitychange`, `window.blur`) detecting external tab searches with progressive strike limits.

---

## 🚀 Quick Start Guide (Run & Demo)

### 1. Prerequisites
- Python 3.10 or higher installed.
- Dependencies installed:
```bash
pip install -r requirements.txt
```
*(Dependencies: `Flask==3.1.3`, `Flask-SQLAlchemy==3.1.1`, `Werkzeug==3.1.3`)*

### 2. Step 1: Initialize Database & Seed Demo Data
Open your terminal (PowerShell or Command Prompt) inside this project folder:
```bash
python seed_data.py
```
*Output: Automatically creates database tables, 3 computer science exams, 35+ multiple choice questions, and pre-configured accounts.*

### 3. Step 2: Run Automated Test Suite
Verify that all 12 unit, integration, and security test cases pass:
```bash
python test_application.py
```
*Output: `Ran 12 tests in ...s - OK`*

### 4. Step 3: Launch the Flask Server
```bash
python run.py
```
*The portal will start running locally at:*  
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Pre-Configured Demo Credentials

| Role | Username / Identifier | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator / Faculty** | `admin@presidency.edu` | `Admin@123` | Create & edit exams, author questions, manage students, view results, export CSV |
| **Student Candidate 1** | `student@presidency.edu` | `Student@123` | View scheduled exams, take live proctored tests, countdown timer, instant scorecards |
| **Student Candidate 2** | `eknath@presidency.edu` | `Student@123` | Test anti-cheat tab-switch detection, review historical grade cards |

*(Students can also self-register through the `/register` portal with instant login access).*

---

## 📂 Project Directory Structure

```
OnlineExaminationSystem/
│
├── api/
│   └── index.py                # Serverless WSGI entrypoint for Vercel deployment
├── app.py                      # Flask Application factory, controller routes & JSON APIs (app = create_app())
├── models.py                   # SQLAlchemy ORM models (User, Exam, Question, ExamResult, StudentAnswer)
├── config.py                   # Environment-aware configuration (PostgreSQL production / SQLite local)
├── seed_data.py                # Database seeder populating exams, questions & demo users
├── run.py                      # Entry point to run local Flask development server
├── requirements.txt            # Python dependencies (Flask, SQLAlchemy, psycopg, gunicorn, etc.)
├── test_application.py         # Automated test suite (12 unit & integration test cases)
├── vercel.json                 # Vercel serverless routing and rewrite rules
├── .vercelignore               # Files excluded from Vercel deployment
├── .python-version             # Pinned Python version (3.12) for Vercel buildpack
├── .env.example                # Template for environment variables (SECRET_KEY, DATABASE_URL)
├── .gitignore                  # Git ignore rules for virtual environments, caches, and secrets
│
├── templates/                  # Jinja2 HTML5 Templates
│   ├── base.html               # Global layout, dark header, navbar & flash alerts
│   ├── index.html              # University landing page with portal credentials
│   ├── login.html              # Role-aware login form (Student vs Admin/Faculty)
│   ├── register.html           # Student self-registration portal
│   ├── student_dashboard.html  # Student dashboard with metrics & available exams
│   ├── exam_instructions.html  # Pre-exam guidelines & honor code pledge
│   ├── exam_screen.html        # Live test console with countdown timer & palette
│   ├── result_detail.html      # Official examination scorecard & question review
│   ├── student_history.html    # Student historical assessment records
│   ├── admin_dashboard.html    # Administrator analytics desk & live feed
│   ├── admin_exams.html        # Exam catalog manager (Create, Edit, Toggle, Delete)
│   ├── admin_exam_form.html    # Exam configuration form (Duration, Marks, Neg. Marking)
│   ├── admin_questions.html    # Question Bank MCQ authoring suite
│   ├── admin_question_edit.html# Question editing form
│   ├── admin_students.html     # Registered student directory & management
│   └── admin_results.html      # Grade roster with filtering & CSV export
│
├── static/                     # Static Client Assets
│   ├── css/
│   │   └── style.css           # Modern university stylesheet (Blue, white, light-grey)
│   └── js/
│       ├── exam.js             # Client test logic: Timer, Palette, Proctor & Autosave
│       └── main.js             # Portal interactivity script
│
├── diagrams/ & Root Assets:
│   ├── usecase_diagram.svg / .png       # UML Use Case Diagram
│   ├── activity_diagram.svg / .png      # UML Activity Diagram
│   ├── er_diagram.svg / .png            # Entity-Relationship (ER) Diagram (5 tables)
│   └── architecture_diagram.svg / .png  # 3-Tier MVC System Architecture Diagram
│
├── UI Screens (1440 × 900 Resolution):
│   ├── screen1_login_reg.svg / .png            # Module 1: Login & Registration
│   ├── screen2_student_dashboard.svg / .png    # Module 2: Student Dashboard
│   ├── screen3_admin_dashboard.svg / .png      # Module 3: Admin & Faculty Desk
│   ├── screen4_online_exam.svg / .png          # Module 4: Live Examination Console
│   └── screen5_result_management.svg / .png    # Module 5: Automated Evaluation & Scorecard
│
├── Online_Examination_System_CSE2271.pptx # 13-slide PPT following university template
├── Project_Report.pdf                     # 7-page formal academic report in PDF
└── PROJECT_DOCUMENTATION.md               # Detailed academic report with Viva Q&A
```

---

## 📊 Core System Modules & Live Workflows

### 1. Student Portal & Exam Attendance Flow:
1. **Login:** Student authenticates via email or university roll number.
2. **Dashboard:** Displays active upcoming tests, attempted examinations, and cumulative percentage.
3. **Instructions & Pledge:** Review course parameters, negative marking policies, and honor pledge.
4. **Live Examination Console:**
   - **Authoritative Countdown Timer:** Synchronized server countdown (`00:42:18`).
   - **4-State Question Palette:** Color-coded status (`Green = Answered`, `Red = Unanswered`, `Orange = Marked for Review`, `Gray = Not Visited`).
   - **Anti-Cheat Proctoring:** Enforces fullscreen mode. Switching tabs or window blur logs an incident warning strike. On the 3rd strike, the test auto-submits immediately.
5. **Instant Evaluation:** Upon submit, the server checks student answers against master keys, applies negative marks (if any), computes percentage, determines pass/fail status, and redirects to the official scorecard.

### 2. Faculty / Administrator Flow:
1. **Dashboard Analytics:** Live metrics of active examinees, total exams, questions in bank, and batch average.
2. **Exam Management:** Create, configure duration, total marks, passing cutoff, and negative marking penalty; toggle between `Published` (Live) and `Draft`.
3. **MCQ Authoring Suite:** Add questions with 4 options, designated answer key, difficulty level, and educational explanations. Edit and delete questions dynamically.
4. **Student Directory:** View registered students, roll numbers, department, semester, and total attempts.
5. **Results & Reporting:** Filter candidate grade cards by course or student; stream download official CSV rosters.

---

## 🛡️ Anti-Cheating & Security Implementation

1. **Zero Client Answer Key Exposure:**  
   The client `/exam/<id>/start` endpoint strips out `correct_option` and `explanation` attributes before serialization. Answer evaluation is strictly server-side.
2. **Tab-Switch & Blur Detection:**  
   JavaScript listens for `document.visibilitychange` and `window.onblur`. Any attempt to open another browser tab or search engine triggers a strike warning.
3. **Single Attempt Guarantee:**  
   Once submitted, `ExamResult.query.filter_by(user_id, exam_id)` blocks duplicate submissions (HTTP 400).
4. **Privacy Isolation:**  
   Students can only access their own results (`/result/<id>`). Attempting to view another candidate's result triggers an unauthorized access redirect.

---

## 🌐 Deployment to GitHub & Vercel (Production Setup)

This application is fully production-configured and serverless-ready for deployment on **Vercel** with a free managed **PostgreSQL** database (such as **Neon**, **Supabase**, or **Vercel Postgres**), while automatically preserving local **SQLite** for offline development.

### Step 1: Create a Free PostgreSQL Database
Because Vercel serverless functions run in a read-only, ephemeral environment without persistent disk storage, production applications must use a cloud database:
1. Sign up for a free cloud PostgreSQL provider:
   - **Neon Serverless Postgres** (Recommended): [neon.tech](https://neon.tech)
   - Or **Supabase**: [supabase.com](https://supabase.com)
   - Or **Vercel Postgres** (accessible directly from your Vercel project dashboard under *Storage*).
2. Copy your PostgreSQL connection URI. It typically looks like:
   ```
   postgresql://username:password@ep-sample-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Push the Project to GitHub
1. Open PowerShell or Command Prompt inside this project folder:
   ```powershell
   cd c:\Users\Eknath\OneDrive\Desktop\OnlineExaminationSystem
   ```
2. Initialize a clean git repository and stage all project files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Online Examination and Result Management System"
   ```
3. Create a new repository on your GitHub account (e.g., `OnlineExaminationSystem`).
4. Link and push your local branch:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/OnlineExaminationSystem.git
   git push -u origin main
   ```

### Step 3: Deploy to Vercel
1. Log in to [vercel.com](https://vercel.com) using your GitHub account.
2. Click **"Add New..."** -> **"Project"**.
3. Locate your `OnlineExaminationSystem` repository from GitHub and click **"Import"**.
4. Leave Framework Preset as **Other** (Vercel automatically detects `vercel.json` and `api/index.py`).
5. Expand the **Environment Variables** section and add:
   - **`SECRET_KEY`**: Set to any secure 32+ character random string (e.g., `presidency-exam-secret-key-2026-secure-token`).
   - **`DATABASE_URL`**: Paste your PostgreSQL connection URI from Step 1.
6. Click **"Deploy"**. Vercel will build the Python serverless bundle and assign your live URL (e.g., `https://online-examination-system-xxx.vercel.app`).

### Step 4: Initialize & Seed the Production Database
For security and performance reasons, demo seeding is **not** run automatically on production boot. To populate your cloud database with the default admin account, sample students, examinations, and question bank:
- Run this one-time command from your local terminal pointing to your remote PostgreSQL database:
  - **PowerShell (Windows):**
    ```powershell
    $env:DATABASE_URL="your-postgresql-connection-uri-here"
    python seed_data.py
    ```
  - **Linux / macOS:**
    ```bash
    DATABASE_URL="your-postgresql-connection-uri-here" python seed_data.py
    ```
- *Output:* Creates all PostgreSQL tables and populates the default faculty administrator and student accounts. You can now log into your live Vercel deployment!

---

## 🎓 Viva Questions & Answers (CSE2271 Defense)

- **Q: What is the benefit of Vanilla JavaScript over React for this examination portal?**  
  *A:* Vanilla JS ensures zero client build dependencies, near-instant rendering on low-spec lab computers, and direct low-level control over browser fullscreen and Page Visibility events without framework abstraction delays.
- **Q: How does the system handle negative marking?**  
  *A:* In `app.py`, incorrect answers deduct `exam.negative_marks_per_q` (e.g. -0.25). Unanswered questions incur 0 deduction. The final score is floored at 0.0 to prevent negative overall grades.
- **Q: How is data corruption prevented during simultaneous submissions?**  
  *A:* SQLite transactions commit `ExamResult` and all `StudentAnswer` records in a single atomic transaction block (`db.session.commit()`). If an error occurs, the session rolls back completely.

---
*Created for Presidency University, Bengaluru — B.Tech Computer Science & Engineering (2026-2027).*
