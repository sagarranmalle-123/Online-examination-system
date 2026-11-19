import os, sys

def clean_ascii(text):
    replacements = {
        '\u2013': '-',
        '\u2014': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2022': '*',
        '•': '*',
        '✓': '[PASS]',
        '✗': '[FAIL]',
        '🔑': '[KEY]',
        '⏱️': '[TIME]',
        '🛡️': '[PROCTOR]',
        '📊': '[METRIC]',
        '✅': '[OK]',
        '⭐': '[STAR]',
        '💡': '[TIP]',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('ascii', 'replace').decode('ascii')

def escape_pdf(text):
    text = clean_ascii(str(text))
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

class MinimalPDF:
    def __init__(self, filename):
        self.filename = filename
        self.pages = []
        self.current_page_stream = []
        self.page_width = 595.28  # A4 Width in points (8.27 in)
        self.page_height = 841.89 # A4 Height in points (11.69 in)
        self.margin = 54.0       # 0.75 in margins
        self.cursor_y = self.page_height - self.margin
        self.page_number = 1

    def new_page(self):
        if self.current_page_stream:
            # Draw header and footer on completed page
            self.draw_page_decorations()
            self.pages.append("".join(self.current_page_stream))
            self.current_page_stream = []
            self.page_number += 1
        self.cursor_y = self.page_height - self.margin - 30

    def draw_page_decorations(self):
        # Header rule & title (pages > 1)
        if self.page_number > 1:
            # Header line
            self.current_page_stream.append(
                f"q 0.2 0.5 0.8 RG 1 w {self.margin} {self.page_height - 40} m {self.page_width - self.margin} {self.page_height - 40} l S Q\n"
            )
            # Header text
            self.current_page_stream.append(
                f"BT /F2 8.5 Tf 0.3 0.4 0.5 rg {self.margin} {self.page_height - 35} Td (Presidency University - CSE2271 Mini-Project Report | Online Examination System) Tj ET\n"
            )
            # Footer line
            self.current_page_stream.append(
                f"q 0.8 0.8 0.8 RG 0.5 w {self.margin} 45 m {self.page_width - self.margin} 45 l S Q\n"
            )
            # Footer text & page number
            self.current_page_stream.append(
                f"BT /F2 8.5 Tf 0.4 0.4 0.4 rg {self.margin} 32 Td (School of Computer Science & Engineering) Tj ET\n"
            )
            p_str = f"Page {self.page_number}"
            self.current_page_stream.append(
                f"BT /F2 8.5 Tf 0.4 0.4 0.4 rg {self.page_width - self.margin - 40} 32 Td ({escape_pdf(p_str)}) Tj ET\n"
            )

    def check_space(self, needed):
        if self.cursor_y - needed < self.margin + 45:
            self.new_page()

    def draw_title(self, text, subtitle=None):
        self.check_space(140)
        # Background card
        box_h = 100 if subtitle else 60
        self.current_page_stream.append(
            f"q 0.06 0.1 0.18 rg {self.margin} {self.cursor_y - box_h} {self.page_width - 2 * self.margin} {box_h} re f Q\n"
        )
        self.current_page_stream.append(
            f"BT /F1 18 Tf 1 1 1 rg {self.margin + 20} {self.cursor_y - 35} Td ({escape_pdf(text)}) Tj ET\n"
        )
        if subtitle:
            self.current_page_stream.append(
                f"BT /F2 10.5 Tf 0.7 0.8 0.9 rg {self.margin + 20} {self.cursor_y - 65} Td ({escape_pdf(subtitle)}) Tj ET\n"
            )
        self.cursor_y -= (box_h + 30)

    def draw_heading1(self, text):
        self.check_space(50)
        self.cursor_y -= 10
        # Blue pill indicator
        self.current_page_stream.append(
            f"q 0.01 0.52 0.78 rg {self.margin} {self.cursor_y - 2} 4 18 re f Q\n"
        )
        self.current_page_stream.append(
            f"BT /F1 14 Tf 0.06 0.1 0.18 rg {self.margin + 12} {self.cursor_y} Td ({escape_pdf(text)}) Tj ET\n"
        )
        self.cursor_y -= 24

    def draw_heading2(self, text):
        self.check_space(40)
        self.cursor_y -= 6
        self.current_page_stream.append(
            f"BT /F1 11.5 Tf 0.06 0.46 0.43 rg {self.margin} {self.cursor_y} Td ({escape_pdf(text)}) Tj ET\n"
        )
        self.cursor_y -= 18

    def draw_paragraph(self, text, size=9.5, color="0.15 0.2 0.25"):
        # Wrap words to fit line
        words = text.split(' ')
        lines = []
        cur_line = []
        max_chars = 95 if size < 10 else 82

        for w in words:
            if len(' '.join(cur_line + [w])) > max_chars:
                lines.append(' '.join(cur_line))
                cur_line = [w]
            else:
                cur_line.append(w)
        if cur_line:
            lines.append(' '.join(cur_line))

        line_height = size * 1.35
        self.check_space(len(lines) * line_height + 8)

        for line in lines:
            self.current_page_stream.append(
                f"BT /F2 {size} Tf {color} rg {self.margin} {self.cursor_y} Td ({escape_pdf(line)}) Tj ET\n"
            )
            self.cursor_y -= line_height
        self.cursor_y -= 6

    def draw_bullet(self, bold_prefix, text, size=9.5):
        line_height = size * 1.35
        full_text = f"• {bold_prefix} {text}"
        words = text.split(' ')
        lines = []
        cur_line = []
        max_chars = 90

        for w in words:
            if len(' '.join(cur_line + [w])) > max_chars:
                lines.append(' '.join(cur_line))
                cur_line = [w]
            else:
                cur_line.append(w)
        if cur_line:
            lines.append(' '.join(cur_line))

        self.check_space((len(lines) + 1) * line_height + 4)

        # Draw bullet and bold prefix
        self.current_page_stream.append(
            f"BT /F1 {size} Tf 0.01 0.52 0.78 rg {self.margin + 8} {self.cursor_y} Td (-) Tj ET\n"
        )
        self.current_page_stream.append(
            f"BT /F1 {size} Tf 0.06 0.1 0.18 rg {self.margin + 20} {self.cursor_y} Td ({escape_pdf(bold_prefix)}) Tj ET\n"
        )
        
        # Calculate offset for prefix
        prefix_offset = len(bold_prefix) * 5.2 + 25
        first_line = lines[0] if lines else ""
        self.current_page_stream.append(
            f"BT /F2 {size} Tf 0.2 0.25 0.3 rg {self.margin + prefix_offset} {self.cursor_y} Td ({escape_pdf(first_line)}) Tj ET\n"
        )
        self.cursor_y -= line_height

        # Remaining lines indented
        for l in lines[1:]:
            self.current_page_stream.append(
                f"BT /F2 {size} Tf 0.2 0.25 0.3 rg {self.margin + 20} {self.cursor_y} Td ({escape_pdf(l)}) Tj ET\n"
            )
            self.cursor_y -= line_height
        self.cursor_y -= 3

    def draw_table(self, headers, rows, col_widths):
        table_width = sum(col_widths)
        row_height = 20
        total_height = (len(rows) + 1) * row_height + 15
        self.check_space(total_height)

        # Table header background
        self.current_page_stream.append(
            f"q 0.06 0.1 0.18 rg {self.margin} {self.cursor_y - row_height} {table_width} {row_height} re f Q\n"
        )

        # Draw Header Text
        cur_x = self.margin
        for idx, h in enumerate(headers):
            self.current_page_stream.append(
                f"BT /F1 9 Tf 1 1 1 rg {cur_x + 6} {self.cursor_y - 14} Td ({escape_pdf(h)}) Tj ET\n"
            )
            cur_x += col_widths[idx]
        self.cursor_y -= row_height

        # Draw Rows
        for r_idx, row in enumerate(rows):
            # Alternating row background
            bg_color = "0.96 0.97 0.98" if r_idx % 2 == 0 else "1 1 1"
            self.current_page_stream.append(
                f"q {bg_color} rg {self.margin} {self.cursor_y - row_height} {table_width} {row_height} re f Q\n"
            )
            # Row bottom line
            self.current_page_stream.append(
                f"q 0.88 0.9 0.92 RG 0.5 w {self.margin} {self.cursor_y - row_height} m {self.margin + table_width} {self.cursor_y - row_height} l S Q\n"
            )

            cur_x = self.margin
            for c_idx, cell in enumerate(row):
                self.current_page_stream.append(
                    f"BT /F2 8.5 Tf 0.15 0.2 0.25 rg {cur_x + 6} {self.cursor_y - 14} Td ({escape_pdf(str(cell))}) Tj ET\n"
                )
                cur_x += col_widths[c_idx]
            self.cursor_y -= row_height
        self.cursor_y -= 12

    def draw_callout_box(self, title, text):
        box_h = 55
        self.check_space(box_h + 15)
        self.current_page_stream.append(
            f"q 0.94 0.97 1 rg 0.01 0.52 0.78 RG 1 w {self.margin} {self.cursor_y - box_h} {self.page_width - 2 * self.margin} {box_h} re B Q\n"
        )
        self.current_page_stream.append(
            f"BT /F1 10.5 Tf 0.01 0.52 0.78 rg {self.margin + 12} {self.cursor_y - 18} Td ({escape_pdf(title)}) Tj ET\n"
        )
        self.current_page_stream.append(
            f"BT /F2 9 Tf 0.1 0.2 0.3 rg {self.margin + 12} {self.cursor_y - 36} Td ({escape_pdf(text)}) Tj ET\n"
        )
        self.cursor_y -= (box_h + 15)

    def save(self):
        # Close last page
        if self.current_page_stream:
            self.draw_page_decorations()
            self.pages.append("".join(self.current_page_stream))

        # Build PDF structure
        objects = []
        
        # 1. Catalog
        objects.append("<< /Type /Catalog /Pages 2 0 R >>")
        
        # 2. Pages
        page_refs = [f"{4 + i * 2} 0 R" for i in range(len(self.pages))]
        objects.append(f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(self.pages)} >>")
        
        # 3. Fonts: F1 = Helvetica-Bold, F2 = Helvetica
        objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")

        # Pages and Streams
        for idx, page_stream in enumerate(self.pages):
            content_id = 5 + idx * 2
            page_obj = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.page_width} {self.page_height}] /Contents {content_id} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> >>"
            objects.append(page_obj)

            stream_bytes = page_stream.encode('latin1', 'replace')
            stream_obj = f"<< /Length {len(stream_bytes)} >>\nstream\n" + page_stream + "\nendstream"
            objects.append(stream_obj)

        # Assemble File
        out = bytearray()
        out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        
        xref_offsets = []
        for i, obj in enumerate(objects):
            xref_offsets.append(len(out))
            out.extend(f"{i + 1} 0 obj\n{obj}\nendobj\n".encode('latin1'))

        xref_pos = len(out)
        out.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode('latin1'))
        for offset in xref_offsets:
            out.extend(f"{offset:010d} 00000 n \n".encode('latin1'))

        trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
        out.extend(trailer.encode('latin1'))

        with open(self.filename, 'wb') as f:
            f.write(out)
        print(f"Successfully generated PDF Report: {self.filename} ({len(self.pages)} Pages)")

def generate_report():
    pdf = MinimalPDF("Project_Report.pdf")

    # ================= COVER PAGE =================
    pdf.cursor_y = 750
    pdf.draw_title(
        "ONLINE EXAMINATION AND RESULT MANAGEMENT SYSTEM",
        "A Secure, Proctored Web Platform for Academic Assessments & Automated Analytics"
    )

    pdf.draw_callout_box(
        "B.Tech CSE Mini-Project Report (Course: CSE2271 - Mini Project Review & Demo)",
        "Submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science & Engineering."
    )

    pdf.draw_heading2("Institutional Details:")
    pdf.draw_paragraph("Institution: Presidency University, Bengaluru")
    pdf.draw_paragraph("School: School of Computer Science & Engineering")
    pdf.draw_paragraph("Academic Year: 2026 – 2027 | Semester: 4th Semester B.Tech (CSE)")
    pdf.draw_paragraph("Course Code & Title: CSE2271 – Mini Project Review & Demo")

    pdf.cursor_y -= 15
    pdf.draw_heading2("Candidate & Review Team:")
    headers = ["Sl. No.", "Candidate Name", "University Roll Number", "Program / Specialization"]
    rows = [
        ["1", "[Student Name 1]", "[Roll Number 1]", "B.Tech Computer Science & Engineering"],
        ["2", "[Student Name 2]", "[Roll Number 2]", "B.Tech Computer Science & Engineering"],
        ["3", "[Student Name 3]", "[Roll Number 3]", "B.Tech Computer Science & Engineering"],
        ["4", "[Student Name 4]", "[Roll Number 4]", "B.Tech Computer Science & Engineering"],
        ["5", "[Student Name 5]", "[Roll Number 5]", "B.Tech Computer Science & Engineering"],
    ]
    pdf.draw_table(headers, rows, [45, 140, 130, 170])

    pdf.draw_paragraph("Faculty Guide / Reviewer: [Faculty Guide / Reviewer Name]")
    pdf.draw_paragraph("Head of Department (HoD): [Head of Department Name]")

    # ================= PAGE 2: ABSTRACT & OBJECTIVES =================
    pdf.new_page()
    pdf.draw_heading1("1. Abstract & Executive Summary")
    pdf.draw_paragraph(
        "The Online Examination and Result Management System is a modern, responsive, and full-stack web application "
        "designed specifically for higher education institutions to conduct secure, automated, and tamper-resistant academic assessments. "
        "Traditional examination systems suffer from severe logistical bottlenecks, paper waste, scheduling delays, manual grading "
        "inconsistencies, and vulnerability to academic dishonesty. This project addresses these challenges by delivering an end-to-end "
        "digital testing platform built strictly with semantic HTML5, CSS3 Grid/Flexbox, Vanilla JavaScript (ES6+), Python Flask, and SQLite "
        "with Flask-SQLAlchemy ORM. No third-party frontend frameworks (such as React, Angular, or Node.js) were employed, ensuring lightweight "
        "footprint, lightning-fast rendering, and complete control over browser events."
    )
    pdf.draw_paragraph(
        "Key highlights include multi-portal Role-Based Access Control (RBAC), synchronized live countdown timer, interactive question palette, "
        "active proctoring with tab-switch and window-blur violation detection (HTML5 Page Visibility API), instant server-authoritative objective "
        "scoring with negative marking support, official PDF/CSV scorecards, and administrative question bank authoring."
    )

    pdf.draw_heading1("2. Problem Statement")
    pdf.draw_paragraph(
        "Conventional university examination systems face several critical challenges:"
    )
    pdf.draw_bullet("Logistical Overhead:", "Physical printing, manual distribution, invigilation coordination, and physical answer booklet storage incur massive operational costs.")
    pdf.draw_bullet("Evaluation Latency:", "Manual evaluation of multiple-choice and objective tests for hundreds of students takes weeks, delaying grade publishing and academic progression.")
    pdf.draw_bullet("Integrity Vulnerabilities:", "Unsupervised online assessments are prone to external browser tab lookups, unauthorized copying, and clock tampering.")
    pdf.draw_bullet("Lack of Performance Analytics:", "Pen-and-paper examinations fail to provide students with granular topic-by-topic mastery breakdown or percentile ranking.")

    pdf.draw_heading1("3. Project Objectives")
    pdf.draw_bullet("Paperless Examination Pipeline:", "Provide seamless paperless exam scheduling, candidate registration, and instant question delivery.")
    pdf.draw_bullet("Strict Multi-Layer Proctoring:", "Enforce fullscreen lockdown and detect external tab switching with progressive strike limits (auto-submit on strike 3).")
    pdf.draw_bullet("Automated Server-Side Grading:", "Compare student choices against master answer keys immediately upon submit, calculating net score with negative marking.")
    pdf.draw_bullet("ACID Database Reliability:", "Ensure zero data loss during peak submission windows using SQLite atomic transactions.")

    # ================= PAGE 3: REQUIREMENTS SPECIFICATION =================
    pdf.new_page()
    pdf.draw_heading1("4. Software Requirements Specification (SRS)")
    pdf.draw_heading2("A. Functional Requirements (10 Core Requirements)")

    fr_data = [
        ["FR01", "User Authentication & RBAC", "Provides distinct portals for Student and Admin roles with salted password hashing (Werkzeug)."],
        ["FR02", "Student Self-Registration", "Enables students to enroll with Full Name, Roll No/PRN, Email, Department, and Semester."],
        ["FR03", "Exam Scheduling & Policies", "Faculty configure test course code, duration, total marks, passing cutoff, and negative marks."],
        ["FR04", "MCQ Question Bank Authoring", "Supports authoring questions with 4 options, master key, mark weightage, and explanations."],
        ["FR05", "Dynamic Publishing Toggle", "Instructors toggle exams between Active Live Window and Draft to control examinee access."],
        ["FR06", "Synchronized Countdown Timer", "Authoritative timer that auto-submits responses and terminates session when reaching 00:00:00."],
        ["FR07", "Interactive Question Palette", "4-state color-coded palette (Answered, Unanswered, Review, Not Visited) with instant question jumping."],
        ["FR08", "Anti-Cheat Tab-Switch Detection", "Detects window blur/tab switches via Page Visibility API; logs strikes and auto-submits on strike 3."],
        ["FR09", "Automatic Net Score Grading", "Evaluates student answers server-side; computes positive marks and negative mark penalties."],
        ["FR10", "Result Analytics & CSV Export", "Generates student scorecards with accuracy and rank; enables faculty to export complete CSV grade rosters."]
    ]
    pdf.draw_table(["Req ID", "Functional Module", "Operational Description"], fr_data, [50, 160, 275])

    pdf.draw_heading2("B. Non-Functional Requirements (6 Core Requirements)")
    nfr_data = [
        ["NFR01", "High Performance & Low Latency", "Page load time < 1.5s; asynchronous JSON test submission processed in < 300 ms."],
        ["NFR02", "Security & Zero Key Leakage", "Passwords stored with cryptographic salt; test JSON payload strictly excludes answer keys."],
        ["NFR03", "Fault Tolerance & Autosave", "Client-side state caching preserves student responses against transient network disconnects."],
        ["NFR04", "Responsive Usability", "Complies with WCAG 2.1 AA accessibility; responsive across desktop 1440x900 and laptops."],
        ["NFR05", "ACID Data Reliability", "SQLite atomic transactions ensure results and individual answers are committed without partial writes."],
        ["NFR06", "Modularity & Maintainability", "Clean separation between Presentation templates, Flask route controllers, and ORM models."]
    ]
    pdf.draw_table(["Req ID", "Quality Attribute", "Specification Metric"], nfr_data, [50, 150, 285])

    # ================= PAGE 4: SYSTEM ARCHITECTURE & DESIGN =================
    pdf.new_page()
    pdf.draw_heading1("5. System Architecture & High-Level Design")
    pdf.draw_paragraph(
        "The application is engineered using the classic 3-Tier Model-View-Controller (MVC) architectural pattern, "
        "ensuring clean separation of concerns, high maintainability, and horizontal scalability."
    )

    pdf.draw_heading2("Layer 1: Presentation Layer (Client Browser)")
    pdf.draw_paragraph(
        "• Semantic HTML5 & CSS3: Implements a clean, university-branded aesthetic using deep blue (#0284c7), slate navy (#0f172a), "
        "white, and subtle light-grey backgrounds (#f8fafc). Layouts utilize CSS Grid for multi-column dashboards and Flexbox for toolbars."
    )
    pdf.draw_paragraph(
        "• Vanilla JavaScript Live Test Console: Coordinates the countdown timer, manages question navigation state (userAnswers map), "
        "monitors HTML5 fullscreen and Page Visibility API events, and handles asynchronous JSON fetch() submissions."
    )

    pdf.draw_heading2("Layer 2: Application / Controller Layer (Python Flask)")
    pdf.draw_paragraph(
        "• Authentication & Session Gatekeeper: Custom decorators (@login_required, @admin_required) enforce strict role separation. "
        "Session identifiers are cryptographically signed using Flask's SECRET_KEY to eliminate session tampering or privilege escalation."
    )
    pdf.draw_paragraph(
        "• Auto-Evaluation Engine (/api/exam/<id>/submit): Receives candidate answer mappings, loads canonical answer keys from SQLite, "
        "grades each question, applies negative marks for errors, floors net score at 0.0, determines pass/fail status, and persists telemetry."
    )
    pdf.draw_paragraph(
        "• Reporting Controller: Computes batch percentile ranks, topic accuracy metrics, and streams dynamic CSV rosters for university administrators."
    )

    pdf.draw_heading2("Layer 3: Data Persistence Layer (SQLite & Flask-SQLAlchemy)")
    pdf.draw_paragraph(
        "• Flask-SQLAlchemy ORM provides object-relational mapping, connection pooling, and parameterized SQL queries to prevent SQL Injection."
    )
    pdf.draw_paragraph(
        "• SQLite 3 engine maintains ACID transactional guarantees. Foreign key cascading rules automatically clean up orphan questions or answers."
    )

    # ================= PAGE 5: DATABASE SCHEMA & ENTITIES =================
    pdf.new_page()
    pdf.draw_heading1("6. Database Design & Entity Schema")
    pdf.draw_paragraph(
        "The relational schema comprises five normalized entities engineered to 3NF standards:"
    )

    db_tables = [
        ["Table Name", "Primary Key", "Foreign Keys", "Key Fields & Purpose"],
        ["users", "id (INTEGER)", "None", "name, roll_no (UNIQUE), email (UNIQUE), password_hash, role ('student'/'admin'), department, semester"],
        ["exams", "id (INTEGER)", "created_by_id -> users.id", "title, course_code, duration_minutes, total_marks, passing_marks, negative_marks_per_q, is_active"],
        ["questions", "id (INTEGER)", "exam_id -> exams.id", "question_text, option_a..d, correct_option ('A'-'D'), marks, explanation, difficulty"],
        ["exam_results", "id (INTEGER)", "user_id -> users.id, exam_id -> exams.id", "score, max_score, percentage, passed, correct/incorrect counts, time_taken_seconds, strike_count"],
        ["student_answers", "id (INTEGER)", "result_id -> exam_results.id, question_id -> questions.id", "selected_option ('A'-'D'/NULL), is_correct (BOOLEAN), marks_awarded (FLOAT)"]
    ]
    pdf.draw_table(db_tables[0], db_tables[1:], [80, 75, 120, 210])

    pdf.draw_heading2("Integrity Constraints & Relationships:")
    pdf.draw_bullet("One-to-Many (users -> exams):", "Faculty user can author multiple exams. Foreign key created_by_id references users.id.")
    pdf.draw_bullet("One-to-Many (exams -> questions):", "An exam aggregates multiple MCQs. Cascade delete ensures deleting an exam removes all associated questions.")
    pdf.draw_bullet("One-to-Many (users -> exam_results):", "A student examinee generates exam results across multiple course assessments.")
    pdf.draw_bullet("One-to-Many (exam_results -> student_answers):", "Every submitted scorecard tracks granular item-level responses for audit and review.")

    # ================= PAGE 6: TESTING MATRIX & VERIFICATION =================
    pdf.new_page()
    pdf.draw_heading1("7. Software Testing & Verification Matrix")
    pdf.draw_paragraph(
        "Automated unit and integration testing was executed using Python's standard unittest test suite (test_application.py). "
        "All 12 test suites passed successfully with 100% assertion coverage:"
    )

    test_matrix = [
        ["Test ID", "Test Case Description", "Input / Action", "Expected Result", "Status"],
        ["TC01", "Password Cryptography", "set_password('Student@123')", "Salted hash generated; plaintext rejected", "PASSED"],
        ["TC02", "Student Registration", "POST /register with valid fields", "User row committed in SQLite; roll no saved", "PASSED"],
        ["TC03", "Duplicate Email Validation", "POST /register with existing email", "Form rejected with warning alert", "PASSED"],
        ["TC04", "Password Mismatch Check", "POST /register with unequal passwords", "Registration aborted with danger flash", "PASSED"],
        ["TC05", "Student Login & Logout", "POST /login valid credentials", "Authenticated session initialized; clean logout", "PASSED"],
        ["TC06", "Admin Desk Barrier", "Student GET /admin/dashboard", "Access denied; redirect to student dashboard", "PASSED"],
        ["TC07", "Exam Creation & Toggle", "POST /admin/exams/create & toggle", "Exam stored; status toggled active/draft", "PASSED"],
        ["TC08", "Question Authoring & Edit", "POST /admin/exams/1/questions", "MCQ added; question fields updated in DB", "PASSED"],
        ["TC09", "Student Directory Mgmt", "GET & POST /admin/students/delete", "Student directory displayed; cascade delete OK", "PASSED"],
        ["TC10", "Zero Answer Key Leakage", "GET /exam/1/start payload", "Correct keys and explanations omitted from JSON", "PASSED"],
        ["TC11", "Auto-Scoring & Negative Marks", "POST /api/exam/1/submit with Q1, Q2", "Calculates net score factoring -0.5 penalty", "PASSED"],
        ["TC12", "Duplicate Retake Prevention", "POST duplicate /api/exam/1/submit", "Rejected with HTTP 400 'Exam already submitted'", "PASSED"]
    ]
    pdf.draw_table(["ID", "Module Under Test", "Test Input", "Expected Outcome", "Status"], test_matrix, [35, 110, 140, 160, 40])

    pdf.draw_callout_box(
        "Verification Summary: 12 of 12 Test Cases Passed (100% Success Rate)",
        "The automated test suite confirms strict role-based isolation, bulletproof answer key confidentiality, and atomic score computation."
    )

    # ================= PAGE 7: CONCLUSION & VIVA GUIDE =================
    pdf.new_page()
    pdf.draw_heading1("8. Design Justification & Viva Defense Guide")
    pdf.draw_paragraph(
        "Key questions and model answers prepared for the CSE2271 Mini-Project Review & Viva demonstration:"
    )

    pdf.draw_bullet(
        "Q1: Why choose Vanilla JS and Flask over React and Node.js?",
        "Vanilla JS eliminates complex toolchains, multi-megabyte bundle downloads, and virtual DOM overhead. For university test consoles, raw DOM access allows direct binding to Fullscreen and Page Visibility events without framework abstraction delays."
    )
    pdf.draw_bullet(
        "Q2: How does the system prevent student cheating during an exam?",
        "A multi-layer strategy is employed: (1) Mandatory fullscreen mode, (2) Page Visibility API listening for tab switches and window blur events, (3) Progressive strikes logged to database, (4) Forced auto-submission on the 3rd strike, (5) Strict server-side grading where answer keys are never sent to the browser."
    )
    pdf.draw_bullet(
        "Q3: How does the system handle negative marking?",
        "For each question, if selected_option == correct_option, marks_awarded = question.marks. If selected_option is wrong, marks_awarded = -exam.negative_marks_per_q. Unanswered questions receive 0. The final score is floored at 0.0 to prevent negative total grades."
    )
    pdf.draw_bullet(
        "Q4: What happens if a student experiences internet disconnection?",
        "Responses are maintained continuously in client JavaScript memory. When connectivity is restored, clicking Save & Next or Submit flushes the active payload. SQLite atomic transactions ensure all answers and the result record are written in one single commit."
    )

    pdf.draw_heading1("9. Conclusion & Future Enhancements")
    pdf.draw_paragraph(
        "The Online Examination and Result Management System successfully achieves all academic objectives outlined in the Presidency University "
        "CSE2271 curriculum. It provides a secure, intuitive, and high-performance portal that automates administrative workflows, enforces test integrity, "
        "and delivers instant feedback to students."
    )
    pdf.draw_heading2("Future Enhancements Roadmap:")
    pdf.draw_bullet("Webcam AI Proctoring:", "Integrate OpenCV facial tracking to detect multiple faces, gaze diversion, or candidate absence.")
    pdf.draw_bullet("Subjective Answer Grading:", "Incorporate Natural Language Processing (NLP) models to automatically evaluate short-answer and coding questions.")
    pdf.draw_bullet("LMS Integration:", "Provide LTI (Learning Tools Interoperability) plugins to synchronize grades with Canvas and Moodle.")

    pdf.save()

if __name__ == '__main__':
    generate_report()
