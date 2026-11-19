import os, zlib, struct

def create_styled_png(width, height, title_text, subtitle_text, theme_color):
    r_t, g_t, b_t = theme_color
    raw = bytearray()
    
    for y in range(height):
        raw.append(0)  # filter type None
        is_border = (y < 4 or y >= height - 4)
        is_header = (y < 60)
        is_footer = (y >= height - 35)
        
        for x in range(width):
            is_col_border = (x < 4 or x >= width - 4)
            if is_border or is_col_border:
                raw.extend([15, 23, 42, 255])
            elif is_header:
                ratio = x / width
                r_h = int(r_t * (1 - ratio * 0.25))
                g_h = int(g_t * (1 - ratio * 0.25))
                b_h = int(b_t * (1 - ratio * 0.25))
                raw.extend([r_h, g_h, b_h, 255])
            elif is_footer:
                raw.extend([241, 245, 249, 255])
            else:
                is_grid = (x % 40 == 0 or y % 40 == 0)
                if is_grid:
                    raw.extend([248, 250, 252, 255])
                else:
                    raw.extend([255, 255, 255, 255])
                    
    compressed = zlib.compress(raw, level=6)
    
    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)
    
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')

def build_er_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" width="1200" height="700">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.1"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1200" height="700" fill="#f8fafc"/>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1200" height="60" fill="#0f172a"/>
  <text x="30" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="bold" fill="#ffffff">ENTITY-RELATIONSHIP (ER) DIAGRAM</text>
  <text x="600" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#94a3b8">Online Examination and Result Management System | SQLite &amp; Flask-SQLAlchemy</text>
  <rect x="1050" y="14" width="120" height="32" rx="16" fill="#0284c7"/>
  <text x="1110" y="35" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">5 Core Tables</text>

  <!-- Table 1: USERS (Top Left) -->
  <g transform="translate(40, 90)" filter="url(#shadow)">
    <rect width="320" height="250" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="320" height="42" rx="8" fill="#0284c7"/>
    <rect y="30" width="320" height="12" fill="#0284c7"/>
    <text x="15" y="27" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff">📋 users</text>
    <text x="305" y="27" font-family="'Segoe UI', sans-serif" font-size="11" fill="#bae6fd" text-anchor="end">Authentication &amp; Profiles</text>

    <!-- Attributes -->
    <text x="15" y="65" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0284c7">🔑 id</text>
    <text x="180" y="65" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (PK, AUTO)</text>
    
    <text x="15" y="87" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   name</text>
    <text x="180" y="87" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(100) NOT NULL</text>

    <text x="15" y="109" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   roll_no</text>
    <text x="180" y="109" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(50) UNIQUE</text>

    <text x="15" y="131" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   email</text>
    <text x="180" y="131" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(120) UNIQUE</text>

    <text x="15" y="153" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   password_hash</text>
    <text x="180" y="153" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(256) NOT NULL</text>

    <text x="15" y="175" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   role</text>
    <text x="180" y="175" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(20) 'student'</text>

    <text x="15" y="197" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   department</text>
    <text x="180" y="197" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(100)</text>

    <text x="15" y="219" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   semester</text>
    <text x="180" y="219" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(20)</text>

    <text x="15" y="241" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   created_at</text>
    <text x="180" y="241" font-family="'Consolas', monospace" font-size="11" fill="#64748b">DATETIME</text>
  </g>

  <!-- Table 2: EXAMS (Top Center-Right) -->
  <g transform="translate(440, 90)" filter="url(#shadow)">
    <rect width="330" height="270" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="330" height="42" rx="8" fill="#0f766e"/>
    <rect y="30" width="330" height="12" fill="#0f766e"/>
    <text x="15" y="27" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff">📝 exams</text>
    <text x="315" y="27" font-family="'Segoe UI', sans-serif" font-size="11" fill="#ccfbf1" text-anchor="end">Exam Catalog &amp; Policies</text>

    <!-- Attributes -->
    <text x="15" y="65" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0f766e">🔑 id</text>
    <text x="185" y="65" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (PK, AUTO)</text>

    <text x="15" y="87" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   title</text>
    <text x="185" y="87" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(200) NOT NULL</text>

    <text x="15" y="109" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   course_code</text>
    <text x="185" y="109" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(50) NOT NULL</text>

    <text x="15" y="131" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   duration_minutes</text>
    <text x="185" y="131" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER DEFAULT 60</text>

    <text x="15" y="153" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   total_marks</text>
    <text x="185" y="153" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT DEFAULT 50.0</text>

    <text x="15" y="175" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   passing_marks</text>
    <text x="185" y="175" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT DEFAULT 20.0</text>

    <text x="15" y="197" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   negative_marks_per_q</text>
    <text x="185" y="197" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT DEFAULT 0.25</text>

    <text x="15" y="219" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   is_active</text>
    <text x="185" y="219" font-family="'Consolas', monospace" font-size="11" fill="#64748b">BOOLEAN DEFAULT 1</text>

    <text x="15" y="241" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0284c7">🔗 created_by_id</text>
    <text x="185" y="241" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> users.id)</text>

    <text x="15" y="263" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   created_at</text>
    <text x="185" y="263" font-family="'Consolas', monospace" font-size="11" fill="#64748b">DATETIME</text>
  </g>

  <!-- Table 3: QUESTIONS (Top Right) -->
  <g transform="translate(840, 90)" filter="url(#shadow)">
    <rect width="320" height="270" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="320" height="42" rx="8" fill="#b45309"/>
    <rect y="30" width="320" height="12" fill="#b45309"/>
    <text x="15" y="27" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff">❓ questions</text>
    <text x="305" y="27" font-family="'Segoe UI', sans-serif" font-size="11" fill="#fef3c7" text-anchor="end">MCQ Question Bank</text>

    <!-- Attributes -->
    <text x="15" y="65" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#b45309">🔑 id</text>
    <text x="180" y="65" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (PK, AUTO)</text>

    <text x="15" y="87" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0f766e">🔗 exam_id</text>
    <text x="180" y="87" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> exams.id)</text>

    <text x="15" y="109" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   question_text</text>
    <text x="180" y="109" font-family="'Consolas', monospace" font-size="11" fill="#64748b">TEXT NOT NULL</text>

    <text x="15" y="131" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   option_a, b, c, d</text>
    <text x="180" y="131" font-family="'Consolas', monospace" font-size="11" fill="#64748b">TEXT NOT NULL</text>

    <text x="15" y="153" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#dc2626">   correct_option</text>
    <text x="180" y="153" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(1) 'A'-'D'</text>

    <text x="15" y="175" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   marks</text>
    <text x="180" y="175" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT DEFAULT 2.0</text>

    <text x="15" y="197" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   explanation</text>
    <text x="180" y="197" font-family="'Consolas', monospace" font-size="11" fill="#64748b">TEXT</text>

    <text x="15" y="219" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   difficulty</text>
    <text x="180" y="219" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(20) 'Medium'</text>
  </g>

  <!-- Table 4: EXAM_RESULTS (Bottom Left-Center) -->
  <g transform="translate(180, 410)" filter="url(#shadow)">
    <rect width="360" height="260" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="360" height="42" rx="8" fill="#15803d"/>
    <rect y="30" width="360" height="12" fill="#15803d"/>
    <text x="15" y="27" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff">🏆 exam_results</text>
    <text x="345" y="27" font-family="'Segoe UI', sans-serif" font-size="11" fill="#bbf7d0" text-anchor="end">Submissions &amp; Grade Cards</text>

    <!-- Attributes -->
    <text x="15" y="65" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#15803d">🔑 id</text>
    <text x="210" y="65" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (PK, AUTO)</text>

    <text x="15" y="87" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0284c7">🔗 user_id</text>
    <text x="210" y="87" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> users.id)</text>

    <text x="15" y="109" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#0f766e">🔗 exam_id</text>
    <text x="210" y="109" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> exams.id)</text>

    <text x="15" y="131" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   score, max_score</text>
    <text x="210" y="131" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT (Net marks)</text>

    <text x="15" y="153" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   percentage, passed</text>
    <text x="210" y="153" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT, BOOLEAN</text>

    <text x="15" y="175" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   correct, incorrect, unanswered</text>
    <text x="210" y="175" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER</text>

    <text x="15" y="197" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   time_taken_seconds</text>
    <text x="210" y="197" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER</text>

    <text x="15" y="219" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   strike_count</text>
    <text x="210" y="219" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (Anti-Cheat)</text>

    <text x="15" y="241" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   submitted_at</text>
    <text x="210" y="241" font-family="'Consolas', monospace" font-size="11" fill="#64748b">DATETIME</text>
  </g>

  <!-- Table 5: STUDENT_ANSWERS (Bottom Right) -->
  <g transform="translate(680, 410)" filter="url(#shadow)">
    <rect width="360" height="200" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="360" height="42" rx="8" fill="#4338ca"/>
    <rect y="30" width="360" height="12" fill="#4338ca"/>
    <text x="15" y="27" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff">🎯 student_answers</text>
    <text x="345" y="27" font-family="'Segoe UI', sans-serif" font-size="11" fill="#c7d2fe" text-anchor="end">Item-Level Response Audit</text>

    <!-- Attributes -->
    <text x="15" y="65" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#4338ca">🔑 id</text>
    <text x="210" y="65" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (PK, AUTO)</text>

    <text x="15" y="87" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#15803d">🔗 result_id</text>
    <text x="210" y="87" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> results.id)</text>

    <text x="15" y="109" font-family="'Consolas', monospace" font-size="12" font-weight="bold" fill="#b45309">🔗 question_id</text>
    <text x="210" y="109" font-family="'Consolas', monospace" font-size="11" fill="#64748b">INTEGER (FK -> questions.id)</text>

    <text x="15" y="131" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   selected_option</text>
    <text x="210" y="131" font-family="'Consolas', monospace" font-size="11" fill="#64748b">VARCHAR(1) NULL ('A'-'D')</text>

    <text x="15" y="153" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   is_correct</text>
    <text x="210" y="153" font-family="'Consolas', monospace" font-size="11" fill="#64748b">BOOLEAN DEFAULT 0</text>

    <text x="15" y="175" font-family="'Consolas', monospace" font-size="12" fill="#0f172a">   marks_awarded</text>
    <text x="210" y="175" font-family="'Consolas', monospace" font-size="11" fill="#64748b">FLOAT (Net Item Score)</text>
  </g>

  <!-- Relationship Connector Paths & Labels -->
  <!-- Users -> Exams (1 : N) -->
  <path d="M 360 170 L 440 170" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="382" y="150" width="36" height="18" rx="4" fill="#e0f2fe"/>
  <text x="400" y="163" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0284c7" text-anchor="middle">1 : N</text>

  <!-- Exams -> Questions (1 : N) -->
  <path d="M 770 170 L 840 170" fill="none" stroke="#0f766e" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="787" y="150" width="36" height="18" rx="4" fill="#ccfbf1"/>
  <text x="805" y="163" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0f766e" text-anchor="middle">1 : N</text>

  <!-- Users -> ExamResults (1 : N) -->
  <path d="M 200 340 L 200 410" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="182" y="365" width="36" height="18" rx="4" fill="#e0f2fe"/>
  <text x="200" y="378" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0284c7" text-anchor="middle">1 : N</text>

  <!-- Exams -> ExamResults (1 : N) -->
  <path d="M 500 360 L 500 410" fill="none" stroke="#0f766e" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="482" y="375" width="36" height="18" rx="4" fill="#ccfbf1"/>
  <text x="500" y="388" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#0f766e" text-anchor="middle">1 : N</text>

  <!-- ExamResults -> StudentAnswers (1 : N) -->
  <path d="M 540 510 L 680 510" fill="none" stroke="#15803d" stroke-width="2" marker-end="url(#arrowGreen)"/>
  <rect x="592" y="490" width="36" height="18" rx="4" fill="#dcfce7"/>
  <text x="610" y="503" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#15803d" text-anchor="middle">1 : N</text>

  <!-- Questions -> StudentAnswers (1 : N) -->
  <path d="M 960 360 L 960 410" fill="none" stroke="#b45309" stroke-width="2" marker-end="url(#arrowAmber)"/>
  <rect x="942" y="375" width="36" height="18" rx="4" fill="#fef3c7"/>
  <text x="960" y="388" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="bold" fill="#b45309" text-anchor="middle">1 : N</text>
</svg>'''

def build_architecture_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" width="1200" height="720">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.1"/>
    </filter>
    <marker id="flowArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1200" height="720" fill="#f8fafc"/>

  <!-- Top Banner -->
  <rect x="0" y="0" width="1200" height="60" fill="#0f172a"/>
  <text x="30" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="bold" fill="#ffffff">SYSTEM ARCHITECTURE (MVC / 3-TIER)</text>
  <text x="560" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#94a3b8">Online Examination and Result Management System | Presidency University (CSE2271)</text>

  <!-- TIER 1: CLIENT PRESENTATION TIER -->
  <g transform="translate(30, 80)" filter="url(#shadow)">
    <rect width="1140" height="120" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="240" height="32" rx="6" fill="#0284c7"/>
    <text x="15" y="21" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">TIER 1: PRESENTATION LAYER</text>

    <!-- Client components -->
    <g transform="translate(20, 45)">
      <rect width="250" height="60" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
      <text x="15" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0369a1">Client Browser View</text>
      <text x="15" y="46" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748b">Semantic HTML5, CSS3 Grid, Flexbox</text>
    </g>

    <g transform="translate(290, 45)">
      <rect width="260" height="60" rx="6" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="15" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#15803d">Live Test Engine (Vanilla JS)</text>
      <text x="15" y="46" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748b">Synced Timer, Palette Jump, Autosave</text>
    </g>

    <g transform="translate(570, 45)">
      <rect width="260" height="60" rx="6" fill="#fef2f2" stroke="#fecaca"/>
      <text x="15" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#b91c1c">Anti-Cheat Proctoring Client</text>
      <text x="15" y="46" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748b">Fullscreen API, Page Visibility Tab Blur</text>
    </g>

    <g transform="translate(850, 45)">
      <rect width="270" height="60" rx="6" fill="#faf5ff" stroke="#e9d5ff"/>
      <text x="15" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#6b21a8">Admin / Faculty Management Desk</text>
      <text x="15" y="46" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748b">Question Authoring, Analytics, CSV Export</text>
    </g>
  </g>

  <!-- Connecting Flow Arrow 1 to 2 -->
  <path d="M 600 200 L 600 235" fill="none" stroke="#0284c7" stroke-width="2.5" marker-end="url(#flowArrow)"/>
  <rect x="520" y="205" width="160" height="20" rx="4" fill="#e0f2fe"/>
  <text x="600" y="219" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#0284c7" text-anchor="middle">HTTP(S) GET / POST &amp; JSON APIs</text>

  <!-- TIER 2: APPLICATION & BUSINESS LOGIC TIER (FLASK BACKEND) -->
  <g transform="translate(30, 240)" filter="url(#shadow)">
    <rect width="1140" height="240" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="300" height="32" rx="6" fill="#0f766e"/>
    <text x="15" y="21" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">TIER 2: APPLICATION / CONTROLLER TIER (FLASK)</text>

    <!-- Sub-modules in Tier 2 -->
    <!-- Module A: Auth & Security -->
    <g transform="translate(20, 50)">
      <rect width="250" height="165" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <rect width="250" height="28" rx="6" fill="#0284c7"/>
      <text x="15" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">🔐 Auth &amp; Session Manager</text>
      <text x="15" y="50" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Role-Based Access Control</text>
      <text x="15" y="70" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Werkzeug salted hash (scrypt)</text>
      <text x="15" y="90" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Flask cryptographically signed cookies</text>
      <text x="15" y="110" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• @login_required decorator</text>
      <text x="15" y="130" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• @admin_required desk barrier</text>
      <text x="15" y="150" font-family="'Segoe UI', sans-serif" font-size="11" fill="#15803d">✓ Zero Privilege Escalation</text>
    </g>

    <!-- Module B: Assessment & Evaluation Controller -->
    <g transform="translate(290, 50)">
      <rect width="260" height="165" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <rect width="260" height="28" rx="6" fill="#15803d"/>
      <text x="15" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">⚡ Evaluation &amp; Grading Engine</text>
      <text x="15" y="50" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Server-side objective answer check</text>
      <text x="15" y="70" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Master key comparison isolation</text>
      <text x="15" y="90" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Negative mark penalty deduction</text>
      <text x="15" y="110" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Floor net score to 0.0</text>
      <text x="15" y="130" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Percentage &amp; Pass/Fail threshold</text>
      <text x="15" y="150" font-family="'Segoe UI', sans-serif" font-size="11" fill="#15803d">✓ Instant Scorecard Computation</text>
    </g>

    <!-- Module C: Proctoring & Telemetry -->
    <g transform="translate(570, 50)">
      <rect width="260" height="165" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <rect width="260" height="28" rx="6" fill="#b91c1c"/>
      <text x="15" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">🛡️ Anti-Cheat &amp; Policy Enforcement</text>
      <text x="15" y="50" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Tab switch &amp; window blur logging</text>
      <text x="15" y="70" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Progressive strike increment (1..3)</text>
      <text x="15" y="90" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Forced auto-submit on strike 3</text>
      <text x="15" y="110" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Single active attempt enforcement</text>
      <text x="15" y="130" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Disallow retake after submission</text>
      <text x="15" y="150" font-family="'Segoe UI', sans-serif" font-size="11" fill="#b91c1c">✓ Complete Test Session Integrity</text>
    </g>

    <!-- Module D: Jinja2 Templating & CSV Export -->
    <g transform="translate(850, 50)">
      <rect width="270" height="165" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <rect width="270" height="28" rx="6" fill="#6b21a8"/>
      <text x="15" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">📊 Reporting &amp; Template Renderer</text>
      <text x="15" y="50" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Jinja2 Dynamic HTML Template Engine</text>
      <text x="15" y="70" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Context Processors (user injection)</text>
      <text x="15" y="90" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Official Candidate Grade Card view</text>
      <text x="15" y="110" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Streaming CSV Result Roster export</text>
      <text x="15" y="130" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">• Batch percentile calculation</text>
      <text x="15" y="150" font-family="'Segoe UI', sans-serif" font-size="11" fill="#6b21a8">✓ Ready for University Registrar</text>
    </g>
  </g>

  <!-- Connecting Flow Arrow 2 to 3 -->
  <path d="M 600 480 L 600 515" fill="none" stroke="#0f766e" stroke-width="2.5" marker-end="url(#flowArrow)"/>
  <rect x="510" y="485" width="180" height="20" rx="4" fill="#ccfbf1"/>
  <text x="600" y="499" font-family="'Segoe UI', sans-serif" font-size="10.5" font-weight="bold" fill="#0f766e" text-anchor="middle">Flask-SQLAlchemy ORM (Python Models)</text>

  <!-- TIER 3: DATA PERSISTENCE & DATABASE ENGINE -->
  <g transform="translate(30, 520)" filter="url(#shadow)">
    <rect width="1140" height="170" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="280" height="32" rx="6" fill="#1e293b"/>
    <text x="15" y="21" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">TIER 3: DATA PERSISTENCE TIER (SQLITE 3)</text>

    <!-- Database Tables and Features -->
    <g transform="translate(20, 45)">
      <rect width="190" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="15" y="25" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0284c7">users</text>
      <text x="15" y="45" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• id (PK), name, email</text>
      <text x="15" y="65" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• roll_no, password_hash</text>
      <text x="15" y="85" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• role, department, sem</text>
    </g>

    <g transform="translate(230, 45)">
      <rect width="200" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="15" y="25" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0f766e">exams</text>
      <text x="15" y="45" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• id (PK), title, code</text>
      <text x="15" y="65" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• duration, total/pass marks</text>
      <text x="15" y="85" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• negative_marks, active</text>
    </g>

    <g transform="translate(450, 45)">
      <rect width="200" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="15" y="25" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#b45309">questions</text>
      <text x="15" y="45" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• id (PK), exam_id (FK)</text>
      <text x="15" y="65" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• question_text, options A-D</text>
      <text x="15" y="85" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• correct_option, marks, exp</text>
    </g>

    <g transform="translate(670, 45)">
      <rect width="210" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="15" y="25" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#15803d">exam_results</text>
      <text x="15" y="45" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• id (PK), user_id, exam_id</text>
      <text x="15" y="65" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• score, percentage, passed</text>
      <text x="15" y="85" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• strikes, time_taken, date</text>
    </g>

    <g transform="translate(900, 45)">
      <rect width="220" height="105" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="15" y="25" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#4338ca">student_answers</text>
      <text x="15" y="45" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• id (PK), result_id (FK)</text>
      <text x="15" y="65" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• question_id (FK)</text>
      <text x="15" y="85" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#64748b">• selected_option, is_correct</text>
    </g>
  </g>
</svg>'''

if __name__ == '__main__':
    # Write SVG files
    with open('er_diagram.svg', 'w', encoding='utf-8') as f:
        f.write(build_er_svg())
    print("Created er_diagram.svg")

    with open('architecture_diagram.svg', 'w', encoding='utf-8') as f:
        f.write(build_architecture_svg())
    print("Created architecture_diagram.svg")

    # Generate PNG files
    er_png = create_styled_png(1200, 700, "ENTITY-RELATIONSHIP DIAGRAM", "SQLite & SQLAlchemy Schema", (15, 118, 110))
    with open('er_diagram.png', 'wb') as f:
        f.write(er_png)
    print("Created er_diagram.png")

    arch_png = create_styled_png(1200, 720, "SYSTEM ARCHITECTURE (MVC)", "3-Tier Scalable System Design", (2, 132, 199))
    with open('architecture_diagram.png', 'wb') as f:
        f.write(arch_png)
    print("Created architecture_diagram.png")
