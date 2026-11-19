import os, zlib, struct

def create_screen_png(width, height, title, subtitle, color):
    r_t, g_t, b_t = color
    raw = bytearray()
    
    for y in range(height):
        raw.append(0)
        is_border = (y < 4 or y >= height - 4)
        is_browser_bar = (y < 42)
        is_app_header = (y >= 42 and y < 100)
        is_footer = (y >= height - 30)
        
        for x in range(width):
            is_col_border = (x < 4 or x >= width - 4)
            if is_border or is_col_border:
                raw.extend([15, 23, 42, 255])
            elif is_browser_bar:
                # Browser chrome bar
                if y < 20 and x < 80:
                    raw.extend([239, 68, 68, 255] if x < 25 else [245, 158, 11, 255] if x < 45 else [16, 185, 129, 255] if x < 65 else [30, 41, 59, 255])
                else:
                    raw.extend([30, 41, 59, 255])
            elif is_app_header:
                ratio = x / width
                r_h = int(r_t * (1 - ratio * 0.2))
                g_h = int(g_t * (1 - ratio * 0.2))
                b_h = int(b_t * (1 - ratio * 0.2))
                raw.extend([r_h, g_h, b_h, 255])
            elif is_footer:
                raw.extend([241, 245, 249, 255])
            else:
                is_grid = (x % 50 == 0 or y % 50 == 0)
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

def build_screen1_login_reg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- Browser Frame Header (1440x900) -->
  <rect width="1440" height="900" fill="#f8fafc"/>
  <rect width="1440" height="42" fill="#1e293b"/>
  <circle cx="24" cy="21" r="6" fill="#ef4444"/>
  <circle cx="44" cy="21" r="6" fill="#f59e0b"/>
  <circle cx="64" cy="21" r="6" fill="#10b981"/>
  <rect x="200" y="8" width="1040" height="26" rx="13" fill="#0f172a"/>
  <text x="720" y="25" font-family="'Segoe UI', monospace, sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">🔒 https://exam.presidencyuniversity.in/login</text>

  <!-- University Global Navigation Header -->
  <rect y="42" width="1440" height="68" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="40" y="56" width="40" height="40" rx="8" fill="#0284c7"/>
  <text x="60" y="83" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text>
  <text x="95" y="75" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#0f172a">PRESIDENCY UNIVERSITY</text>
  <text x="95" y="93" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">School of Computer Science &amp; Engineering | Examination Portal</text>
  <rect x="1220" y="58" width="180" height="36" rx="18" fill="#e0f2fe"/>
  <text x="1310" y="81" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#0284c7" text-anchor="middle">Academic Session 2026-27</text>

  <!-- Hero Intro Section -->
  <rect x="40" y="130" width="1360" height="90" rx="12" fill="#0f172a" filter="url(#shadow)"/>
  <text x="70" y="168" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff">Online Examination &amp; Result Management Portal</text>
  <text x="70" y="195" font-family="'Segoe UI', sans-serif" font-size="13" fill="#94a3b8">B.Tech Computer Science &amp; Engineering | Secure Role-Based Academic Authentication Desk</text>
  <rect x="1190" y="152" width="180" height="42" rx="21" fill="#0284c7"/>
  <text x="1280" y="178" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">🛡️ SSL 256-Bit Encrypted</text>

  <!-- Two Main Cards: Login (Left) & Registration (Right) -->
  <!-- Card 1: Secure Login Form -->
  <g transform="translate(40, 245)" filter="url(#shadow)">
    <rect width="660" height="610" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="660" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="660" height="15" fill="#f8fafc"/>
    <text x="30" y="36" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">1. Authenticate to Portal</text>
    <rect x="520" y="14" width="115" height="28" rx="14" fill="#dcfce7"/>
    <text x="577" y="33" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#166534" text-anchor="middle">ACTIVE DIRECTORY</text>

    <!-- Role Toggle Pills -->
    <rect x="30" y="75" width="295" height="40" rx="8" fill="#0284c7"/>
    <text x="177" y="100" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">👨‍🎓 Student Role</text>
    <rect x="335" y="75" width="295" height="40" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="482" y="100" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#64748b" text-anchor="middle">🛡️ Faculty / Admin Role</text>

    <!-- Email / Roll Input -->
    <text x="30" y="150" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#334155">University Roll No / PRN or Email Address *</text>
    <rect x="30" y="162" width="600" height="48" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="45" y="192" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">student@presidency.edu (or 20241CSE0750)</text>

    <!-- Password Input -->
    <text x="30" y="240" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#334155">Master Account Password *</text>
    <rect x="30" y="252" width="600" height="48" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="45" y="282" font-family="'Segoe UI', monospace, sans-serif" font-size="16" fill="#0f172a">••••••••••••</text>

    <!-- Remember & Forgot Password -->
    <rect x="30" y="320" width="16" height="16" rx="4" fill="#0284c7"/>
    <text x="55" y="333" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Remember session on this computer</text>
    <text x="630" y="333" font-family="'Segoe UI', sans-serif" font-size="12" fill="#0284c7" text-anchor="end">Forgot Password?</text>

    <!-- Submit Button -->
    <rect x="30" y="360" width="600" height="50" rx="8" fill="#0284c7"/>
    <text x="330" y="391" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">LOG IN TO EXAMINATION SYSTEM ➔</text>

    <!-- Demo Credentials Helper Box -->
    <rect x="30" y="440" width="600" height="140" rx="8" fill="#f0f9ff" stroke="#bae6fd"/>
    <text x="45" y="468" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0369a1">🔑 Pre-Configured Demo Credentials for Academic Evaluation:</text>
    <text x="45" y="498" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Student Account:</tspan> <code>student@presidency.edu</code> / <code>Student@123</code></text>
    <text x="45" y="525" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Second Student:</tspan> <code>eknath@presidency.edu</code> / <code>Student@123</code></text>
    <text x="45" y="552" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Faculty / Admin:</tspan> <code>admin@presidency.edu</code> / <code>Admin@123</code></text>
  </g>

  <!-- Card 2: Student Registration Form (Right) -->
  <g transform="translate(740, 245)" filter="url(#shadow)">
    <rect width="660" height="610" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="660" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="660" height="15" fill="#f8fafc"/>
    <text x="30" y="36" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">2. New Student Registration</text>
    <rect x="535" y="14" width="100" height="28" rx="14" fill="#e0f2fe"/>
    <text x="585" y="33" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">SELF-ENROLL</text>

    <!-- Full Name & Roll Number -->
    <text x="30" y="85" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Full Candidate Name *</text>
    <rect x="30" y="95" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="42" y="122" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">Student Candidate</text>

    <text x="340" y="85" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">University Roll No / PRN *</text>
    <rect x="340" y="95" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="352" y="122" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">20241CSE0750</text>

    <!-- University Email -->
    <text x="30" y="160" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Official University Email Address *</text>
    <rect x="30" y="170" width="600" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="42" y="197" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">candidate@presidency.edu</text>

    <!-- Department & Semester Dropdowns -->
    <text x="30" y="235" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Academic Department *</text>
    <rect x="30" y="245" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="42" y="272" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">Computer Science &amp; Engg</text>

    <text x="340" y="235" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Current Semester *</text>
    <rect x="340" y="245" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="352" y="272" font-family="'Segoe UI', sans-serif" font-size="13" fill="#0f172a">4th Semester (B.Tech)</text>

    <!-- Password & Confirm Password -->
    <text x="30" y="310" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Create Password *</text>
    <rect x="30" y="320" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="42" y="347" font-family="'Segoe UI', monospace, sans-serif" font-size="15" fill="#0f172a">••••••••••••</text>

    <text x="340" y="310" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#334155">Confirm Password *</text>
    <rect x="340" y="320" width="290" height="42" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="352" y="347" font-family="'Segoe UI', monospace, sans-serif" font-size="15" fill="#0f172a">••••••••••••</text>

    <!-- Honor Code Checkbox -->
    <rect x="30" y="385" width="16" height="16" rx="4" fill="#059669"/>
    <text x="55" y="398" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155">I agree to abide by Presidency University Academic Honor Code &amp; Test Proctoring Rules.</text>

    <!-- Register Button -->
    <rect x="30" y="425" width="600" height="50" rx="8" fill="#0f766e"/>
    <text x="330" y="456" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">COMPLETE REGISTRATION ➔</text>

    <!-- System Requirements Notice -->
    <rect x="30" y="495" width="600" height="85" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>
    <text x="45" y="522" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">SYSTEM REQUIREMENTS FOR TEST SESSIONS:</text>
    <text x="45" y="545" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#475569">• Modern web browser (Chrome, Edge, Firefox) with JavaScript &amp; Cookies enabled.</text>
    <text x="45" y="565" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#475569">• Fullscreen mode is mandatory. Real-time tab-switch detection logs strikes.</text>
  </g>
</svg>'''

def build_screen2_student_dashboard():
    # High-resolution 1440x900 student dashboard
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Browser Chrome (1440x900) -->
  <rect width="1440" height="900" fill="#f8fafc"/>
  <rect width="1440" height="42" fill="#1e293b"/>
  <circle cx="24" cy="21" r="6" fill="#ef4444"/>
  <circle cx="44" cy="21" r="6" fill="#f59e0b"/>
  <circle cx="64" cy="21" r="6" fill="#10b981"/>
  <rect x="200" y="8" width="1040" height="26" rx="13" fill="#0f172a"/>
  <text x="720" y="25" font-family="'Segoe UI', monospace, sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">🔒 https://exam.presidencyuniversity.in/student/dashboard</text>

  <!-- University Navigation Header -->
  <rect y="42" width="1440" height="68" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="40" y="56" width="40" height="40" rx="8" fill="#0284c7"/>
  <text x="60" y="83" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text>
  <text x="95" y="75" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#0f172a">PRESIDENCY UNIVERSITY</text>
  <text x="95" y="93" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">School of Computer Science &amp; Engineering | Student Portal</text>

  <!-- User Pill -->
  <rect x="1170" y="56" width="230" height="40" rx="20" fill="#f1f5f9" stroke="#cbd5e1"/>
  <circle cx="1192" cy="76" r="14" fill="#0284c7"/>
  <text x="1192" y="81" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">ST</text>
  <text x="1215" y="72" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0f172a">Student Candidate</text>
  <text x="1215" y="87" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#0284c7">Roll: 20241CSE0750</text>

  <!-- Module Navigation Tab Bar -->
  <rect y="110" width="1440" height="48" fill="#0f172a"/>
  <text x="40" y="139" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#94a3b8">STUDENT PORTAL:</text>
  <rect x="170" y="118" width="150" height="32" rx="6" fill="#0284c7"/>
  <text x="245" y="139" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">📊 My Dashboard</text>
  <text x="380" y="139" font-family="'Segoe UI', sans-serif" font-size="13" fill="#cbd5e1">📜 Examination History</text>

  <!-- Welcome Banner -->
  <g transform="translate(40, 180)" filter="url(#shadow)">
    <rect width="1360" height="85" rx="10" fill="#0f172a"/>
    <text x="35" y="38" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff">Welcome back, Student Candidate!</text>
    <text x="35" y="62" font-family="'Segoe UI', sans-serif" font-size="13" fill="#94a3b8">B.Tech Computer Science &amp; Engineering | 4th Semester | Roll No: 20241CSE0750</text>
    <rect x="1180" y="24" width="150" height="36" rx="18" fill="#0284c7"/>
    <text x="1255" y="47" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">Academic Status: OK</text>
  </g>

  <!-- 3 Quick Metric Cards -->
  <g transform="translate(40, 285)">
    <!-- Metric 1 -->
    <rect x="0" y="0" width="430" height="110" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <rect x="25" y="25" width="60" height="60" rx="8" fill="#e0f2fe"/>
    <text x="55" y="63" font-size="28" text-anchor="middle">⏱️</text>
    <text x="105" y="45" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">AVAILABLE EXAMINATIONS</text>
    <text x="105" y="78" font-family="'Segoe UI', sans-serif" font-size="30" font-weight="bold" fill="#0284c7">03</text>
    <text x="155" y="76" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Active window open</text>

    <!-- Metric 2 -->
    <rect x="465" y="0" width="430" height="110" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <rect x="490" y="25" width="60" height="60" rx="8" fill="#dcfce7"/>
    <text x="520" y="63" font-size="28" text-anchor="middle">✅</text>
    <text x="570" y="45" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">EXAMINATIONS ATTEMPTED</text>
    <text x="570" y="78" font-family="'Segoe UI', sans-serif" font-size="30" font-weight="bold" fill="#15803d">01</text>
    <text x="620" y="76" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Passed (Score: 18.0 / 20.0)</text>

    <!-- Metric 3 -->
    <rect x="930" y="0" width="430" height="110" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <rect x="955" y="25" width="60" height="60" rx="8" fill="#fef3c7"/>
    <text x="985" y="63" font-size="28" text-anchor="middle">⭐</text>
    <text x="1035" y="45" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">CUMULATIVE AVERAGE</text>
    <text x="1035" y="78" font-family="'Segoe UI', sans-serif" font-size="30" font-weight="bold" fill="#d97706">90.0%</text>
    <text x="1145" y="76" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Grade O (Distinction)</text>
  </g>

  <!-- Scheduled Examinations Table Card -->
  <g transform="translate(40, 420)" filter="url(#shadow)">
    <rect width="1360" height="440" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1360" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="1360" height="15" fill="#f8fafc"/>
    <text x="30" y="36" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">Scheduled Examination Assessments</text>
    <rect x="1200" y="14" width="130" height="28" rx="14" fill="#e0f2fe"/>
    <text x="1265" y="33" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">OFFICIAL ROSTER</text>

    <!-- Table Header -->
    <rect x="30" y="75" width="1300" height="40" fill="#f1f5f9" rx="6"/>
    <text x="50" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">COURSE CODE</text>
    <text x="200" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">EXAMINATION TITLE</text>
    <text x="640" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">DURATION</text>
    <text x="760" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">TOTAL MARKS</text>
    <text x="890" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">PASS CUTOFF</text>
    <text x="1020" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">STATUS</text>
    <text x="1180" y="100" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">ACTION</text>

    <!-- Row 1: CSE2271 -->
    <rect x="30" y="125" width="1300" height="85" fill="#f8fafc" stroke="#e2e8f0" rx="6"/>
    <rect x="45" y="145" width="85" height="30" rx="6" fill="#0284c7"/>
    <text x="87" y="165" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">CSE2271</text>
    <text x="200" y="152" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">System Architecture, UML Modeling &amp; Software Design</text>
    <text x="200" y="174" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">Mid-Term Assessment | 10 Questions | Negative Marking: -0.25</text>
    <text x="640" y="163" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">45 Mins</text>
    <text x="760" y="163" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">20.0 Marks</text>
    <text x="890" y="163" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">8.0 Marks</text>
    <rect x="1015" y="147" width="95" height="26" rx="13" fill="#dcfce7"/>
    <text x="1062" y="164" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">COMPLETED</text>
    <rect x="1160" y="145" width="145" height="34" rx="6" fill="#15803d"/>
    <text x="1232" y="167" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">View Scorecard ➔</text>

    <!-- Row 2: CSE2500 -->
    <rect x="30" y="220" width="1300" height="85" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <rect x="45" y="240" width="85" height="30" rx="6" fill="#0f766e"/>
    <text x="87" y="260" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">CSE2500</text>
    <text x="200" y="247" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Relational Database Systems &amp; SQL Query Optimization</text>
    <text x="200" y="269" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">ACID Properties, Normalization, Query Indexing | 10 Questions</text>
    <text x="640" y="258" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">45 Mins</text>
    <text x="760" y="258" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">20.0 Marks</text>
    <text x="890" y="258" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">8.0 Marks</text>
    <rect x="1015" y="242" width="95" height="26" rx="13" fill="#e0f2fe"/>
    <text x="1062" y="259" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">AVAILABLE</text>
    <rect x="1160" y="240" width="145" height="34" rx="6" fill="#0284c7"/>
    <text x="1232" y="262" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Start Exam ➔</text>

    <!-- Row 3: CSE2102 -->
    <rect x="30" y="315" width="1300" height="85" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <rect x="45" y="335" width="85" height="30" rx="6" fill="#4338ca"/>
    <text x="87" y="355" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">CSE2102</text>
    <text x="200" y="342" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Data Structures &amp; Algorithmic Analysis</text>
    <text x="200" y="364" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">Trees, Graphs, Asymptotic Complexity, Dynamic Programming | 10 Questions</text>
    <text x="640" y="353" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">45 Mins</text>
    <text x="760" y="353" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">20.0 Marks</text>
    <text x="890" y="353" font-family="'Segoe UI', sans-serif" font-size="13" fill="#334155">8.0 Marks</text>
    <rect x="1015" y="337" width="95" height="26" rx="13" fill="#e0f2fe"/>
    <text x="1062" y="354" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#0369a1" text-anchor="middle">AVAILABLE</text>
    <rect x="1160" y="335" width="145" height="34" rx="6" fill="#0284c7"/>
    <text x="1232" y="357" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Start Exam ➔</text>
  </g>
</svg>'''

def build_screen3_admin_dashboard():
    # 1440x900 Admin Dashboard
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Browser Chrome (1440x900) -->
  <rect width="1440" height="900" fill="#f8fafc"/>
  <rect width="1440" height="42" fill="#1e293b"/>
  <circle cx="24" cy="21" r="6" fill="#ef4444"/>
  <circle cx="44" cy="21" r="6" fill="#f59e0b"/>
  <circle cx="64" cy="21" r="6" fill="#10b981"/>
  <rect x="200" y="8" width="1040" height="26" rx="13" fill="#0f172a"/>
  <text x="720" y="25" font-family="'Segoe UI', monospace, sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">🔒 https://exam.presidencyuniversity.in/admin/dashboard</text>

  <!-- University Navigation Header -->
  <rect y="42" width="1440" height="68" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="40" y="56" width="40" height="40" rx="8" fill="#0f766e"/>
  <text x="60" y="83" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text>
  <text x="95" y="75" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#0f172a">PRESIDENCY UNIVERSITY</text>
  <text x="95" y="93" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">School of Computer Science &amp; Engineering | Administrator &amp; Faculty Desk</text>

  <!-- User Pill -->
  <rect x="1170" y="56" width="230" height="40" rx="20" fill="#f1f5f9" stroke="#cbd5e1"/>
  <circle cx="1192" cy="76" r="14" fill="#0f766e"/>
  <text x="1192" y="81" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">AD</text>
  <text x="1215" y="72" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0f172a">Dr. Faculty Head</text>
  <text x="1215" y="87" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#0f766e">🛡️ Administrator</text>

  <!-- Admin Nav Tab Bar -->
  <rect y="110" width="1440" height="48" fill="#0f172a"/>
  <text x="40" y="139" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#94a3b8">ADMIN DESK:</text>
  <rect x="150" y="118" width="130" height="32" rx="6" fill="#0f766e"/>
  <text x="215" y="139" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">📊 Dashboard</text>
  <text x="340" y="139" font-family="'Segoe UI', sans-serif" font-size="13" fill="#cbd5e1">📝 Manage Exams</text>
  <text x="490" y="139" font-family="'Segoe UI', sans-serif" font-size="13" fill="#cbd5e1">👥 Manage Students</text>
  <text x="650" y="139" font-family="'Segoe UI', sans-serif" font-size="13" fill="#cbd5e1">🏆 All Student Results</text>

  <!-- 4 Admin KPI Cards -->
  <g transform="translate(40, 180)">
    <!-- KPI 1 -->
    <rect x="0" y="0" width="315" height="100" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="25" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">TOTAL REGISTERED STUDENTS</text>
    <text x="25" y="70" font-family="'Segoe UI', sans-serif" font-size="32" font-weight="bold" fill="#0284c7">142</text>
    <text x="95" y="68" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Active Examinees</text>

    <!-- KPI 2 -->
    <rect x="348" y="0" width="315" height="100" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="373" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">ACTIVE EXAMINATIONS</text>
    <text x="373" y="70" font-family="'Segoe UI', sans-serif" font-size="32" font-weight="bold" fill="#0f766e">03</text>
    <text x="425" y="68" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Published on Portal</text>

    <!-- KPI 3 -->
    <rect x="696" y="0" width="315" height="100" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="721" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">AUTHORED QUESTIONS</text>
    <text x="721" y="70" font-family="'Segoe UI', sans-serif" font-size="32" font-weight="bold" fill="#b45309">35</text>
    <text x="775" y="68" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">MCQs in Question Bank</text>

    <!-- KPI 4 -->
    <rect x="1045" y="0" width="315" height="100" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="1070" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">AVERAGE BATCH SCORE</text>
    <text x="1070" y="70" font-family="'Segoe UI', sans-serif" font-size="32" font-weight="bold" fill="#15803d">82.4%</text>
    <text x="1190" y="68" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Passing Rate 94%</text>
  </g>

  <!-- Left Column: Active Examinations Management (Width 660) -->
  <g transform="translate(40, 305)" filter="url(#shadow)">
    <rect width="660" height="555" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="660" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="660" height="15" fill="#f8fafc"/>
    <text x="25" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Course Examinations Overview</text>
    <rect x="520" y="12" width="120" height="32" rx="6" fill="#0f766e"/>
    <text x="580" y="33" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">+ New Exam</text>

    <!-- Exam Item 1 -->
    <rect x="25" y="75" width="610" height="135" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>
    <text x="45" y="105" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#0f172a">CSE2271: System Architecture &amp; UML Design</text>
    <text x="45" y="128" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">10 Questions | 45 Mins | Total: 20.0 Marks | Negative: -0.25</text>
    <rect x="45" y="148" width="95" height="24" rx="12" fill="#dcfce7"/>
    <text x="92" y="164" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">● Published</text>
    <rect x="360" y="148" width="125" height="28" rx="4" fill="#0284c7"/>
    <text x="422" y="167" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">Manage MCQs (10)</text>
    <rect x="495" y="148" width="70" height="28" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="530" y="167" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155" text-anchor="middle">Edit</text>
    <rect x="575" y="148" width="65" height="28" rx="4" fill="#fee2e2" stroke="#fca5a5"/>
    <text x="607" y="167" font-family="'Segoe UI', sans-serif" font-size="11" fill="#dc2626" text-anchor="middle">Delete</text>

    <!-- Exam Item 2 -->
    <rect x="25" y="230" width="610" height="135" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="45" y="260" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#0f172a">CSE2500: Database Systems &amp; SQL Query Optimization</text>
    <text x="45" y="283" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">10 Questions | 45 Mins | Total: 20.0 Marks | Negative: -0.25</text>
    <rect x="45" y="303" width="95" height="24" rx="12" fill="#dcfce7"/>
    <text x="92" y="319" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">● Published</text>
    <rect x="360" y="303" width="125" height="28" rx="4" fill="#0284c7"/>
    <text x="422" y="322" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">Manage MCQs (10)</text>
    <rect x="495" y="303" width="70" height="28" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="530" y="322" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155" text-anchor="middle">Edit</text>
    <rect x="575" y="303" width="65" height="28" rx="4" fill="#fee2e2" stroke="#fca5a5"/>
    <text x="607" y="322" font-family="'Segoe UI', sans-serif" font-size="11" fill="#dc2626" text-anchor="middle">Delete</text>

    <!-- Exam Item 3 -->
    <rect x="25" y="385" width="610" height="135" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="45" y="415" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#0f172a">CSE2102: Data Structures &amp; Algorithmic Analysis</text>
    <text x="45" y="438" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">15 Questions | 45 Mins | Total: 20.0 Marks | Negative: -0.25</text>
    <rect x="45" y="458" width="95" height="24" rx="12" fill="#dcfce7"/>
    <text x="92" y="474" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">● Published</text>
    <rect x="360" y="458" width="125" height="28" rx="4" fill="#0284c7"/>
    <text x="422" y="477" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">Manage MCQs (15)</text>
    <rect x="495" y="458" width="70" height="28" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="530" y="477" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155" text-anchor="middle">Edit</text>
    <rect x="575" y="458" width="65" height="28" rx="4" fill="#fee2e2" stroke="#fca5a5"/>
    <text x="607" y="477" font-family="'Segoe UI', sans-serif" font-size="11" fill="#dc2626" text-anchor="middle">Delete</text>
  </g>

  <!-- Right Column: Recent Submissions & Proctor Alerts (Width 670) -->
  <g transform="translate(730, 305)" filter="url(#shadow)">
    <rect width="670" height="555" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="670" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="670" height="15" fill="#f8fafc"/>
    <text x="25" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Real-Time Submissions Roster</text>
    <rect x="515" y="12" width="135" height="32" rx="6" fill="#0284c7"/>
    <text x="582" y="33" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">📥 Export CSV</text>

    <!-- Submission 1 -->
    <rect x="25" y="75" width="620" height="75" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>
    <circle cx="55" cy="112" r="18" fill="#e0f2fe"/>
    <text x="55" y="117" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#0284c7" text-anchor="middle">ST</text>
    <text x="85" y="103" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Student Candidate (20241CSE0750)</text>
    <text x="85" y="125" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">CSE2271 | Submitted 2 mins ago | 0 Proctor Strikes</text>
    <text x="580" y="105" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#15803d">18.0 / 20.0</text>
    <text x="580" y="125" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d">90% PASSED</text>

    <!-- Submission 2 -->
    <rect x="25" y="165" width="620" height="75" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
    <circle cx="55" cy="202" r="18" fill="#dcfce7"/>
    <text x="55" y="207" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#15803d" text-anchor="middle">EK</text>
    <text x="85" y="193" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Eknath (20241CSE0752)</text>
    <text x="85" y="215" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">CSE2271 | Submitted 15 mins ago | 1 Proctor Warning</text>
    <text x="580" y="195" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#15803d">19.0 / 20.0</text>
    <text x="580" y="215" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d">95% PASSED</text>

    <!-- Live Proctor Alert Feed Subcard -->
    <rect x="25" y="260" width="620" height="270" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
    <rect x="25" y="260" width="620" height="35" rx="8" fill="#1e293b"/>
    <text x="40" y="283" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">🛡️ REAL-TIME PROCTOR TELEMETRY AUDIT FEED</text>

    <text x="45" y="325" font-family="'Consolas', monospace" font-size="11" fill="#dc2626">● 15:42:10 [ALERT]</text>
    <text x="175" y="325" font-family="'Segoe UI', sans-serif" font-size="12" fill="#0f172a">Candidate 20241CSE0752 triggered window blur event (External tab switched).</text>

    <text x="45" y="360" font-family="'Consolas', monospace" font-size="11" fill="#f59e0b">● 15:35:04 [WARN]</text>
    <text x="175" y="360" font-family="'Segoe UI', sans-serif" font-size="12" fill="#0f172a">Candidate 20241CSE0750 exited fullscreen mode via ESC key. Warning strike logged.</text>

    <text x="45" y="395" font-family="'Consolas', monospace" font-size="11" fill="#2563eb">● 15:20:00 [EVENT]</text>
    <text x="175" y="395" font-family="'Segoe UI', sans-serif" font-size="12" fill="#0f172a">Examination CSE2271 started with 142 authorized examinees.</text>

    <text x="45" y="430" font-family="'Consolas', monospace" font-size="11" fill="#15803d">● 15:18:12 [STATUS]</text>
    <text x="175" y="430" font-family="'Segoe UI', sans-serif" font-size="12" fill="#0f172a">All question bank keys verified and hashed for session integrity.</text>

    <rect x="45" y="465" width="580" height="40" rx="6" fill="#0284c7"/>
    <text x="335" y="490" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">View Full University Examination Grade Roster ➔</text>
  </g>
</svg>'''

def build_screen4_online_exam():
    # 1440x900 Live Examination Console
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.1"/>
    </filter>
  </defs>

  <!-- Browser Chrome (1440x900) -->
  <rect width="1440" height="900" fill="#f8fafc"/>
  <rect width="1440" height="42" fill="#1e293b"/>
  <circle cx="24" cy="21" r="6" fill="#ef4444"/>
  <circle cx="44" cy="21" r="6" fill="#f59e0b"/>
  <circle cx="64" cy="21" r="6" fill="#10b981"/>
  <rect x="200" y="8" width="1040" height="26" rx="13" fill="#0f172a"/>
  <text x="720" y="25" font-family="'Segoe UI', monospace, sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">🔒 https://exam.presidencyuniversity.in/exam/1/start [PROCTORED SESSION]</text>

  <!-- Live Exam Top Status Bar -->
  <rect y="42" width="1440" height="64" fill="#0f172a"/>
  <text x="40" y="72" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff">CSE2271: System Architecture, UML Modeling &amp; Software Design</text>
  <text x="40" y="93" font-family="'Segoe UI', sans-serif" font-size="12" fill="#94a3b8">Candidate: Student Candidate (20241CSE0750) | Presidency Examination Server</text>

  <!-- Countdown Timer Display Center -->
  <rect x="620" y="50" width="230" height="48" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="645" y="80" font-size="20">⏱️</text>
  <text x="675" y="81" font-family="'Segoe UI', monospace, sans-serif" font-size="20" font-weight="bold" fill="#f59e0b">00:42:18</text>
  <text x="780" y="80" font-family="'Segoe UI', sans-serif" font-size="11" fill="#94a3b8">LEFT</text>

  <!-- Proctoring Status Badge & Submit Button -->
  <rect x="1100" y="54" width="150" height="40" rx="20" fill="#064e3b" stroke="#10b981"/>
  <text x="1175" y="79" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#34d399" text-anchor="middle">🛡️ Proctor: Active</text>
  <rect x="1270" y="54" width="130" height="40" rx="8" fill="#dc2626"/>
  <text x="1335" y="79" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">SUBMIT EXAM</text>

  <!-- Left Main Column: Active Question Card (Width 960) -->
  <g transform="translate(40, 130)" filter="url(#shadow)">
    <rect width="960" height="730" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Question Top Bar -->
    <rect width="960" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="960" height="15" fill="#f8fafc"/>
    <text x="30" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#0284c7">QUESTION 08 OF 10</text>
    <rect x="790" y="12" width="140" height="30" rx="15" fill="#e0f2fe"/>
    <text x="860" y="32" font-family="'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="#0369a1" text-anchor="middle">Marks: +2.0, -0.25</text>

    <!-- Question Stem -->
    <text x="35" y="95" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">Which data structure is primarily utilized to implement Breadth First Search (BFS)</text>
    <text x="35" y="125" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">in a graph traversal algorithm to discover vertices in shortest-distance order?</text>

    <!-- Option A -->
    <rect x="35" y="165" width="890" height="70" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <circle cx="70" cy="200" r="14" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
    <text x="100" y="206" font-family="'Segoe UI', sans-serif" font-size="15" fill="#1e293b">A.   Stack (LIFO Order)</text>

    <!-- Option B (Selected Option) -->
    <rect x="35" y="250" width="890" height="70" rx="8" fill="#eff6ff" stroke="#0284c7" stroke-width="2.5"/>
    <circle cx="70" cy="285" r="14" fill="#0284c7"/>
    <circle cx="70" cy="285" r="6" fill="#ffffff"/>
    <text x="100" y="291" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#0284c7">B.   Queue (FIFO Order - Active Selection)</text>

    <!-- Option C -->
    <rect x="35" y="335" width="890" height="70" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <circle cx="70" cy="370" r="14" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
    <text x="100" y="376" font-family="'Segoe UI', sans-serif" font-size="15" fill="#1e293b">C.   Binary Search Tree (Hierarchical Sorting)</text>

    <!-- Option D -->
    <rect x="35" y="420" width="890" height="70" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <circle cx="70" cy="455" r="14" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
    <text x="100" y="461" font-family="'Segoe UI', sans-serif" font-size="15" fill="#1e293b">D.   Priority Queue (Min-Heap Order)</text>

    <!-- Clear Selection & Review Checkbox -->
    <rect x="35" y="520" width="16" height="16" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <text x="60" y="533" font-family="'Segoe UI', sans-serif" font-size="13" fill="#64748b">Mark question for review later</text>
    <text x="925" y="533" font-family="'Segoe UI', sans-serif" font-size="13" fill="#dc2626" text-anchor="end">Clear Selection</text>

    <!-- Navigation Buttons -->
    <rect x="35" y="640" width="160" height="50" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
    <text x="115" y="671" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#475569" text-anchor="middle">← Previous</text>

    <rect x="210" y="640" width="160" height="50" rx="8" fill="#fef3c7" stroke="#fcd34d"/>
    <text x="290" y="671" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#b45309" text-anchor="middle">⭐ Mark Review</text>

    <rect x="765" y="640" width="160" height="50" rx="8" fill="#0284c7"/>
    <text x="845" y="671" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">Save &amp; Next →</text>
  </g>

  <!-- Right Column: Interactive Question Palette (Width 370) -->
  <g transform="translate(1030, 130)" filter="url(#shadow)">
    <rect width="370" height="730" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="370" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="370" height="15" fill="#f8fafc"/>
    <text x="25" y="36" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#0f172a">Question Palette Navigation</text>

    <!-- Palette Legend -->
    <g transform="translate(25, 75)">
      <circle cx="10" cy="10" r="8" fill="#15803d"/>
      <text x="25" y="14" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#334155">Answered (7)</text>

      <circle cx="130" cy="10" r="8" fill="#dc2626"/>
      <text x="145" y="14" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#334155">Unanswered (1)</text>

      <circle cx="250" cy="10" r="8" fill="#d97706"/>
      <text x="265" y="14" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#334155">Review (1)</text>

      <circle cx="10" cy="35" r="8" fill="#e2e8f0" stroke="#94a3b8"/>
      <text x="25" y="39" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#334155">Not Visited (1)</text>
    </g>

    <!-- Palette Grid: 10 Questions -->
    <g transform="translate(25, 140)">
      <!-- Q1 Answered -->
      <rect x="0" y="0" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="27" y="34" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">01</text>

      <!-- Q2 Answered -->
      <rect x="68" y="0" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="95" y="34" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">02</text>

      <!-- Q3 Answered -->
      <rect x="136" y="0" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="163" y="34" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">03</text>

      <!-- Q4 Answered -->
      <rect x="204" y="0" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="231" y="34" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">04</text>

      <!-- Q5 Answered -->
      <rect x="272" y="0" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="299" y="34" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">05</text>

      <!-- Q6 Marked Review -->
      <rect x="0" y="68" width="55" height="55" rx="8" fill="#d97706"/>
      <text x="27" y="102" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">06</text>

      <!-- Q7 Answered -->
      <rect x="68" y="68" width="55" height="55" rx="8" fill="#15803d"/>
      <text x="95" y="102" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">07</text>

      <!-- Q8 Current (Highlighted) -->
      <rect x="136" y="68" width="55" height="55" rx="8" fill="#0284c7" stroke="#0f172a" stroke-width="3"/>
      <text x="163" y="102" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">08</text>

      <!-- Q9 Unanswered -->
      <rect x="204" y="68" width="55" height="55" rx="8" fill="#dc2626"/>
      <text x="231" y="102" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">09</text>

      <!-- Q10 Not Visited -->
      <rect x="272" y="68" width="55" height="55" rx="8" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
      <text x="299" y="102" font-family="'Segoe UI', sans-serif" font-size="16" font-weight="bold" fill="#64748b" text-anchor="middle">10</text>
    </g>

    <!-- Anti-Cheat Status Subcard -->
    <g transform="translate(25, 300)">
      <rect width="320" height="240" rx="8" fill="#f0fdf4" stroke="#86efac"/>
      <rect width="320" height="32" rx="8" fill="#15803d"/>
      <text x="15" y="21" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#ffffff">🛡️ REAL-TIME PROCTOR MONITOR</text>

      <text x="15" y="55" font-family="'Segoe UI', sans-serif" font-size="12" fill="#166534">● Fullscreen Lockdown: Active</text>
      <text x="15" y="80" font-family="'Segoe UI', sans-serif" font-size="12" fill="#166534">● Page Focus: Maintained</text>
      <text x="15" y="105" font-family="'Segoe UI', sans-serif" font-size="12" fill="#166534">● Violations / Strikes: 0 of 3</text>
      <text x="15" y="130" font-family="'Segoe UI', sans-serif" font-size="12" fill="#166534">● Clipboard Copy/Paste: Disabled</text>

      <rect x="15" y="150" width="290" height="70" rx="6" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="25" y="175" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d">PROCTOR WARNING POLICY:</text>
      <text x="25" y="195" font-family="'Segoe UI', sans-serif" font-size="10.5" fill="#334155">Switching browser tabs or exiting fullscreen logs a strike. On 3rd strike, the test auto-submits.</text>
    </g>

    <!-- Big Submit Exam CTA Button -->
    <rect x="25" y="640" width="320" height="50" rx="8" fill="#dc2626"/>
    <text x="185" y="671" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">SUBMIT &amp; FINISH EXAM ➔</text>
  </g>
</svg>'''

def build_screen5_result_management():
    # 1440x900 Result Management & Official Scorecard
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Browser Chrome (1440x900) -->
  <rect width="1440" height="900" fill="#f8fafc"/>
  <rect width="1440" height="42" fill="#1e293b"/>
  <circle cx="24" cy="21" r="6" fill="#ef4444"/>
  <circle cx="44" cy="21" r="6" fill="#f59e0b"/>
  <circle cx="64" cy="21" r="6" fill="#10b981"/>
  <rect x="200" y="8" width="1040" height="26" rx="13" fill="#0f172a"/>
  <text x="720" y="25" font-family="'Segoe UI', monospace, sans-serif" font-size="12" fill="#94a3b8" text-anchor="middle">🔒 https://exam.presidencyuniversity.in/result/1 [OFFICIAL SCORECARD]</text>

  <!-- University Navigation Header -->
  <rect y="42" width="1440" height="68" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="40" y="56" width="40" height="40" rx="8" fill="#0284c7"/>
  <text x="60" y="83" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text>
  <text x="95" y="75" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#0f172a">PRESIDENCY UNIVERSITY</text>
  <text x="95" y="93" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">School of Computer Science &amp; Engineering | Result &amp; Analytics Desk</text>

  <rect x="1220" y="56" width="180" height="40" rx="8" fill="#0284c7"/>
  <text x="1310" y="81" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">📥 Export PDF Scorecard</text>

  <!-- Result Summary Banner -->
  <g transform="translate(40, 130)" filter="url(#shadow)">
    <rect width="1360" height="95" rx="12" fill="#0f172a"/>
    <text x="35" y="42" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="bold" fill="#ffffff">Official Examination Scorecard: CSE2271</text>
    <text x="35" y="68" font-family="'Segoe UI', sans-serif" font-size="13" fill="#94a3b8">Candidate: Student Candidate (Roll: 20241CSE0750) | Submitted: 11-Nov-2026 15:45 | Status: PASSED (Grade O)</text>
    <rect x="1190" y="28" width="140" height="40" rx="20" fill="#15803d"/>
    <text x="1260" y="53" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✓ PASSED</text>
  </g>

  <!-- 4 Top Score Metric Cards -->
  <g transform="translate(40, 245)">
    <!-- Card 1: Score -->
    <rect x="0" y="0" width="320" height="115" rx="10" fill="#ffffff" stroke="#86efac" stroke-width="2" filter="url(#shadow)"/>
    <text x="25" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#15803d">TOTAL MARKS OBTAINED</text>
    <text x="25" y="75" font-family="'Segoe UI', sans-serif" font-size="36" font-weight="bold" fill="#15803d">18.0 <tspan font-size="20" fill="#64748b">/ 20.0</tspan></text>
    <text x="25" y="98" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#15803d">Percentage: 90.0% (Grade O)</text>

    <!-- Card 2: Rank -->
    <rect x="346" y="0" width="320" height="115" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="371" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">CLASS RANK &amp; PERCENTILE</text>
    <text x="371" y="75" font-family="'Segoe UI', sans-serif" font-size="36" font-weight="bold" fill="#0284c7">#03 <tspan font-size="18" fill="#64748b">of 142</tspan></text>
    <text x="371" y="98" font-family="'Segoe UI', sans-serif" font-size="12" fill="#15803d">Top 2.1% of B.Tech CSE Class</text>

    <!-- Card 3: Accuracy -->
    <rect x="693" y="0" width="320" height="115" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="718" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">ACCURACY BREAKDOWN</text>
    <text x="718" y="75" font-family="'Segoe UI', sans-serif" font-size="34" font-weight="bold" fill="#0f172a">90.0%</text>
    <text x="718" y="98" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">9 Correct | 1 Incorrect | 0 Skipped</text>

    <!-- Card 4: Efficiency -->
    <rect x="1040" y="0" width="320" height="115" rx="10" fill="#ffffff" stroke="#cbd5e1" filter="url(#shadow)"/>
    <text x="1065" y="32" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#64748b">TIME CONSUMPTION</text>
    <text x="1065" y="75" font-family="'Segoe UI', sans-serif" font-size="34" font-weight="bold" fill="#0f172a">22m 45s</text>
    <text x="1065" y="98" font-family="'Segoe UI', sans-serif" font-size="12" fill="#64748b">Avg 2m 16s per Question</text>
  </g>

  <!-- Detailed Question-by-Question Review List -->
  <g transform="translate(40, 380)" filter="url(#shadow)">
    <rect width="1360" height="490" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1360" height="55" rx="12" fill="#f8fafc"/>
    <rect y="40" width="1360" height="15" fill="#f8fafc"/>
    <text x="30" y="36" font-family="'Segoe UI', sans-serif" font-size="17" font-weight="bold" fill="#0f172a">Item-Level Response Verification &amp; Solutions Review</text>
    <rect x="1200" y="14" width="130" height="28" rx="14" fill="#dcfce7"/>
    <text x="1265" y="33" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="bold" fill="#15803d" text-anchor="middle">VERIFIED AUDIT</text>

    <!-- Review Item 1: Correct -->
    <g transform="translate(30, 75)">
      <rect width="1300" height="120" rx="8" fill="#f0fdf4" stroke="#86efac"/>
      <rect x="15" y="15" width="30" height="30" rx="15" fill="#15803d"/>
      <text x="30" y="35" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✓</text>
      <text x="60" y="34" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Question 1: Which UML diagram describes the dynamic sequence of messages exchanged between objects over time?</text>
      <text x="1200" y="34" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#15803d">+2.0 Marks</text>

      <text x="60" y="65" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Your Answer:</tspan> B) Sequence Diagram <tspan fill="#15803d" font-weight="bold">(Correct)</tspan> | <tspan font-weight="bold">Master Key:</tspan> B) Sequence Diagram</text>
      <rect x="60" y="78" width="1220" height="30" rx="4" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="75" y="98" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#166534">💡 <tspan font-weight="bold">Faculty Rationale:</tspan> Sequence diagrams emphasize the time ordering of message interactions along object lifelines.</text>
    </g>

    <!-- Review Item 2: Incorrect (Negative Marking Demo) -->
    <g transform="translate(30, 210)">
      <rect width="1300" height="120" rx="8" fill="#fef2f2" stroke="#fca5a5"/>
      <rect x="15" y="15" width="30" height="30" rx="15" fill="#dc2626"/>
      <text x="30" y="35" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✗</text>
      <text x="60" y="34" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Question 2: In relational database normalization, which normal form eliminates transitive functional dependencies?</text>
      <text x="1200" y="34" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#dc2626">-0.25 Marks</text>

      <text x="60" y="65" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Your Answer:</tspan> B) 2NF <tspan fill="#dc2626" font-weight="bold">(Incorrect)</tspan> | <tspan font-weight="bold">Designated Master Key:</tspan> <tspan fill="#15803d" font-weight="bold">C) Third Normal Form (3NF)</tspan></text>
      <rect x="60" y="78" width="1220" height="30" rx="4" fill="#ffffff" stroke="#fecaca"/>
      <text x="75" y="98" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#991b1b">💡 <tspan font-weight="bold">Faculty Rationale:</tspan> 2NF eliminates partial dependencies on candidate keys. 3NF removes transitive non-key dependencies (X -> Y -> Z).</text>
    </g>

    <!-- Review Item 3: Correct -->
    <g transform="translate(30, 345)">
      <rect width="1300" height="120" rx="8" fill="#f0fdf4" stroke="#86efac"/>
      <rect x="15" y="15" width="30" height="30" rx="15" fill="#15803d"/>
      <text x="30" y="35" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✓</text>
      <text x="60" y="34" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Question 3: What is the worst-case asymptotic time complexity of searching an element in an unsorted array of N elements?</text>
      <text x="1200" y="34" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold" fill="#15803d">+2.0 Marks</text>

      <text x="60" y="65" font-family="'Segoe UI', sans-serif" font-size="12" fill="#334155"><tspan font-weight="bold">Your Answer:</tspan> D) O(N) <tspan fill="#15803d" font-weight="bold">(Correct)</tspan> | <tspan font-weight="bold">Master Key:</tspan> D) O(N)</text>
      <rect x="60" y="78" width="1220" height="30" rx="4" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="75" y="98" font-family="'Segoe UI', sans-serif" font-size="11.5" fill="#166534">💡 <tspan font-weight="bold">Faculty Rationale:</tspan> Linear search checks each element sequentially from index 0 to N-1 in the worst case.</text>
    </g>
  </g>
</svg>'''

if __name__ == '__main__':
    screens = [
        ('screen1_login_reg.svg', 'screen1_login_reg.png', build_screen1_login_reg(), 'LOGIN & REGISTRATION', (2, 132, 199)),
        ('screen2_student_dashboard.svg', 'screen2_student_dashboard.png', build_screen2_student_dashboard(), 'STUDENT DASHBOARD', (2, 132, 199)),
        ('screen3_admin_dashboard.svg', 'screen3_admin_dashboard.png', build_screen3_admin_dashboard(), 'ADMIN DESK', (15, 118, 110)),
        ('screen4_online_exam.svg', 'screen4_online_exam.png', build_screen4_online_exam(), 'LIVE EXAMINATION CONSOLE', (220, 38, 38)),
        ('screen5_result_management.svg', 'screen5_result_management.png', build_screen5_result_management(), 'RESULT & SCORECARD', (21, 128, 61)),
    ]

    for svg_file, png_file, svg_content, title, color in screens:
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"Created {svg_file}")

        png_bytes = create_screen_png(1440, 900, title, "Presidency Online Exam System", color)
        with open(png_file, 'wb') as f:
            f.write(png_bytes)
        print(f"Created {png_file}")

        # Also update module1_ui ... module5_ui copies
        mod_idx = screens.index((svg_file, png_file, svg_content, title, color)) + 1
        m_svg = f"module{mod_idx}_ui.svg"
        m_png = f"module{mod_idx}_ui.png"
        with open(m_svg, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        with open(m_png, 'wb') as f:
            f.write(png_bytes)
        print(f"Synchronized {m_svg} and {m_png}")
