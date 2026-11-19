import zipfile, os, shutil
import xml.etree.ElementTree as ET

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
pptx_template = r'C:\Users\Eknath\.gemini\antigravity\brain\abc573df-1225-455c-9407-5179ef509cf8\.user_uploaded\media_1794493875752_16f69b6e.pptx'
output_pptx = os.path.join(BASE_DIR, 'Online_Examination_System_CSE2271.pptx')
work_dir = os.path.join(BASE_DIR, 'pptx_build_temp')

if os.path.exists(work_dir):
    shutil.rmtree(work_dir)

with zipfile.ZipFile(pptx_template, 'r') as z:
    z.extractall(work_dir)

print("Extracted template to:", work_dir)

media_dir = os.path.join(work_dir, 'ppt', 'media')
os.makedirs(media_dir, exist_ok=True)

# Copy all images into ppt/media
images_to_copy = [
    'usecase_diagram.png', 'usecase_diagram.svg',
    'activity_diagram.png', 'activity_diagram.svg',
    'er_diagram.png', 'er_diagram.svg',
    'architecture_diagram.png', 'architecture_diagram.svg',
    'screen1_login_reg.png', 'screen1_login_reg.svg',
    'screen2_student_dashboard.png', 'screen2_student_dashboard.svg',
    'screen3_admin_dashboard.png', 'screen3_admin_dashboard.svg',
    'screen4_online_exam.png', 'screen4_online_exam.svg',
    'screen5_result_management.png', 'screen5_result_management.svg',
    'module1_ui.png', 'module1_ui.svg',
    'module2_ui.png', 'module2_ui.svg',
    'module3_ui.png', 'module3_ui.svg',
    'module4_ui.png', 'module4_ui.svg',
    'module5_ui.png', 'module5_ui.svg'
]

for img in images_to_copy:
    if os.path.exists(os.path.join(BASE_DIR, img)):
        shutil.copyfile(os.path.join(BASE_DIR, img), os.path.join(media_dir, img))

# Ensure [Content_Types].xml includes png and svg
ct_path = os.path.join(work_dir, '[Content_Types].xml')
with open(ct_path, 'r', encoding='utf-8') as f:
    ct_content = f.read()

if '<Default Extension="png"' not in ct_content:
    ct_content = ct_content.replace('</Types>', '<Default Extension="png" ContentType="image/png"/><Default Extension="svg" ContentType="image/svg+xml"/></Types>')
    with open(ct_path, 'w', encoding='utf-8') as f:
        f.write(ct_content)

def xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# Update Slide 2: Project Title & Team Details Placeholders
s2_path = os.path.join(work_dir, 'ppt', 'slides', 'slide2.xml')
with open(s2_path, 'r', encoding='utf-8') as f:
    s2 = f.read()

s2 = s2.replace('Library Management System', 'Online Examination and Result Management System')
s2 = s2.replace('TEAM NO.:', 'TEAM NO.: CSE2271-TEAM-10')

# Clean placeholders for team members
team_placeholders = [
    ('1', '[Student Name 1]', '[Roll Number 1]'),
    ('2', '[Student Name 2]', '[Roll Number 2]'),
    ('3', '[Student Name 3]', '[Roll Number 3]'),
    ('4', '[Student Name 4]', '[Roll Number 4]'),
    ('5', '[Student Name 5]', '[Roll Number 5]'),
]

for num, name, roll in team_placeholders:
    target = f'<a:t>{num}</a:t>'
    replacement = f'<a:t>{num}</a:t></a:r></a:p></a:txBody></a:tc><a:tc><a:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-IN" sz="1400" b="1"/><a:t>{name}</a:t></a:r></a:p></a:txBody></a:tc><a:tc><a:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-IN" sz="1400" b="1"/><a:t>{roll}</a:t>'
    s2 = s2.replace(target, replacement)

with open(s2_path, 'w', encoding='utf-8') as f:
    f.write(s2)
print("Updated Slide 2 with team placeholders.")

# Bullet maker for FR and NFR
def make_bullet_body(items, bullet_color="0284C7"):
    paras = []
    for title, desc in items:
        p_xml = f'''<a:p>
          <a:pPr marL="342900" indent="-250000">
            <a:buClr><a:srgbClr val="{bullet_color}"/></a:buClr>
            <a:buSzPts val="1600"/>
            <a:buChar char="●"/>
          </a:pPr>
          <a:r>
            <a:rPr lang="en-US" b="1" sz="1350">
              <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
              <a:latin typeface="Segoe UI"/>
            </a:rPr>
            <a:t>{title} </a:t>
          </a:r>
          <a:r>
            <a:rPr lang="en-US" sz="1250">
              <a:solidFill><a:srgbClr val="334155"/></a:solidFill>
              <a:latin typeface="Segoe UI"/>
            </a:rPr>
            <a:t>{desc}</a:t>
          </a:r>
        </a:p>'''
        paras.append(p_xml)
    return f'''<a:bodyPr spcFirstLastPara="1" wrap="square" lIns="91425" tIns="45700" rIns="91425" bIns="45700" anchor="t" anchorCtr="0"><a:normAutofit/></a:bodyPr><a:lstStyle/>{''.join(paras)}'''

# Update Slide 4: Functional Requirements
s4_path = os.path.join(work_dir, 'ppt', 'slides', 'slide4.xml')
fr_items = [
    ("FR01. User Authentication &amp; Role-Based Access Control:", "Secure multi-portal access for Student and Administrator/Faculty roles with Werkzeug salted password hashing."),
    ("FR02. Student Self-Registration:", "Examinees self-register with University Roll No/PRN, Email, Academic Department, and Semester."),
    ("FR03. Examination Parameter Configuration:", "Faculty configure test duration (minutes), total marks, passing cutoff, and negative marking penalty."),
    ("FR04. MCQ Question Bank Authoring:", "Comprehensive MCQ authoring suite with 4 options, designated answer key, mark weightage, and explanation."),
    ("FR05. Exam Publishing &amp; Access Window Toggling:", "Dynamic publishing control allowing examiners to toggle tests between Active Live Window and Draft."),
    ("FR06. Synchronized Live Countdown Timer:", "Authoritative countdown timer automatically auto-submits answers and terminates session when reaching 00:00:00."),
    ("FR07. Question Palette &amp; Navigation Matrix:", "Color-coded 4-state question palette (Answered, Unanswered, Marked for Review, Not Visited) with instant question jumping."),
    ("FR08. Real-Time Anti-Cheat Proctoring:", "HTML5 Page Visibility API detects tab-switching and window blurs; logs strikes and auto-submits on the 3rd strike."),
    ("FR09. Instant Automated Scoring Engine:", "Evaluates student choices server-side against database answer keys factoring in positive marks and negative mark deductions."),
    ("FR10. Result Analytics &amp; Grade Card Roster:", "Instant student scorecard with rank, accuracy, and topic breakdown; faculty can filter and export all results to CSV.")
]

with open(s4_path, 'r', encoding='utf-8') as f:
    s4 = f.read()

idx_start = s4.find('<a:bodyPr', s4.find('id="115"'))
idx_end = s4.find('</p:txBody>', idx_start)
s4 = s4[:idx_start] + make_bullet_body(fr_items, "0284C7") + s4[idx_end:]

with open(s4_path, 'w', encoding='utf-8') as f:
    f.write(s4)
print("Updated Slide 4: Functional Requirements.")

# Update Slide 5: Non-Functional Requirements
s5_path = os.path.join(work_dir, 'ppt', 'slides', 'slide5.xml')
nfr_items = [
    ("NFR01. Performance &amp; Sub-Second Latency:", "Page load times under 1.5s; lightweight asynchronous JSON answer submissions completed in &lt; 300 ms."),
    ("NFR02. Security &amp; Anti-Tampering Integrity:", "Cryptographic password hashing (scrypt/pbkdf2), session isolation, and strict server-side evaluation with zero answer key leakage."),
    ("NFR03. High Availability &amp; State Persistence:", "Zero response loss; candidate selections are cached locally to tolerate transient Wi-Fi disconnects or page refreshes."),
    ("NFR04. Usability &amp; Responsive University UI:", "Clean WCAG-compliant design with modern university blue/white/grey palette; responsive desktop and tablet view."),
    ("NFR05. ACID Transactional Data Reliability:", "SQLite atomic commits guarantee exam results and individual student answers are persisted together without corruption."),
    ("NFR06. Modularity &amp; Architectural Cleanliness:", "Separation of Presentation templates, Flask route controllers, and SQLAlchemy database models.")
]

with open(s5_path, 'r', encoding='utf-8') as f:
    s5 = f.read()

idx_start = s5.find('<a:bodyPr', s5.find('id="115"'))
idx_end = s5.find('</p:txBody>', idx_start)
s5 = s5[:idx_start] + make_bullet_body(nfr_items, "0F766E") + s5[idx_end:]

with open(s5_path, 'w', encoding='utf-8') as f:
    f.write(s5)
print("Updated Slide 5: Non-Functional Requirements.")

# Function to safely embed pictures into slides
def embed_image_in_slide(slide_num, title_text, png_name, svg_name, shape_id):
    s_path = os.path.join(work_dir, 'ppt', 'slides', f'slide{slide_num}.xml')
    rels_path = os.path.join(work_dir, 'ppt', 'slides', '_rels', f'slide{slide_num}.xml.rels')

    with open(rels_path, 'r', encoding='utf-8') as f:
        rels = f.read()

    # Find highest existing rId
    import re
    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
    max_rid = max(rids) if rids else 1
    png_rid = f"rId{max_rid + 1}"
    svg_rid = f"rId{max_rid + 2}"

    new_rel_entries = f'<Relationship Id="{png_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{png_name}"/><Relationship Id="{svg_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{svg_name}"/>'
    rels = rels.replace('</Relationships>', new_rel_entries + '</Relationships>')

    with open(rels_path, 'w', encoding='utf-8') as f:
        f.write(rels)

    with open(s_path, 'r', encoding='utf-8') as f:
        s_xml = f.read()

    # Update slide title
    if title_text:
        idx_t = s_xml.find('<a:t>', s_xml.find('id="114"'))
        idx_t_end = s_xml.find('</a:t>', idx_t)
        if idx_t != -1:
            s_xml = s_xml[:idx_t+5] + xml_escape(title_text) + s_xml[idx_t_end:]

    # Replace shape 115 with picture
    idx_sp = s_xml.find('<p:sp>', s_xml.find('id="115"') - 120)
    idx_sp_end = s_xml.find('</p:sp>', idx_sp) + 7

    pic_xml = f'''<p:pic>
      <p:nvPicPr>
        <p:cNvPr id="{shape_id}" name="Figure_{slide_num}"/>
        <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
        <p:nvPr/>
      </p:nvPicPr>
      <p:blipFill>
        <a:blip r:embed="{png_rid}">
          <a:extLst>
            <a:ext uri="{{28A0092B-C50C-407E-A947-70E740481C1C}}">
              <a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/>
            </a:ext>
            <a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">
              <asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{svg_rid}"/>
            </a:ext>
          </a:extLst>
        </a:blip>
        <a:stretch><a:fillRect/></a:stretch>
      </p:blipFill>
      <p:spPr>
        <a:xfrm>
          <a:off x="812800" y="850000"/>
          <a:ext cx="10566400" cy="5650000"/>
        </a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
    </p:pic>'''

    s_xml = s_xml[:idx_sp] + pic_xml + s_xml[idx_sp_end:]
    with open(s_path, 'w', encoding='utf-8') as f:
        f.write(s_xml)
    print(f"Embedded image into Slide {slide_num}: {png_name}")

# Slide 6: Use Case Diagram
embed_image_in_slide(6, "Usecase Diagram", "usecase_diagram.png", "usecase_diagram.svg", 306)

# Slide 7: Activity Diagram
embed_image_in_slide(7, "Activity Diagram", "activity_diagram.png", "activity_diagram.svg", 307)

# Slide 8: UI Screen 1 - Login and Registration
embed_image_in_slide(8, "Design four to five User Interface Screens – Module 1: Login & Registration", "screen1_login_reg.png", "screen1_login_reg.svg", 308)

# Slide 9: UI Screen 2 - Student Dashboard
embed_image_in_slide(9, "Design four to five User Interface Screens – Module 2: Student Dashboard", "screen2_student_dashboard.png", "screen2_student_dashboard.svg", 309)

# Slide 10: UI Screen 3 - Admin Dashboard
embed_image_in_slide(10, "Design four to five User Interface Screens – Module 3: Admin & Faculty Desk", "screen3_admin_dashboard.png", "screen3_admin_dashboard.svg", 310)

# Slide 11: UI Screen 4 - Online Examination Console
embed_image_in_slide(11, "Design four to five User Interface Screens – Module 4: Live Examination Console", "screen4_online_exam.png", "screen4_online_exam.svg", 311)

# Slide 12: UI Screen 5 - Result Management & Analytics
embed_image_in_slide(12, "Design four to five User Interface Screens – Module 5: Automated Evaluation & Scorecard", "screen5_result_management.png", "screen5_result_management.svg", 312)

# Update Slide 13: Design Justification (3-5 minutes)
s13_path = os.path.join(work_dir, 'ppt', 'slides', 'slide13.xml')
justification_items = [
    ("1. Academic Motivation &amp; Need:", "Eliminates pen-and-paper overhead, prevents grading bias, and automates institutional evaluation workflows for CSE2271."),
    ("2. 3-Tier MVC Architecture:", "Strict separation of responsive HTML5 UI, Python Flask controllers, and SQLite database models enables independent scalability."),
    ("3. Authoritative Server-Side Timing:", "Prevents local clock manipulation; exam duration countdown and submission windows are strictly verified by backend server timestamps."),
    ("4. Multi-Layer Anti-Cheat Proctoring:", "HTML5 Page Visibility API and Fullscreen locks detect tab switching with progressive warning strikes and forced auto-submission on strike 3."),
    ("5. Fault-Tolerant Client Autosave:", "Responses are cached locally in JavaScript state to survive accidental browser refreshes and transient network disconnects."),
    ("6. Instant Objective Evaluation:", "Calculates raw score, negative marking penalties, percentile ranking, and generates official student scorecards instantaneously.")
]

with open(s13_path, 'r', encoding='utf-8') as f:
    s13 = f.read()

idx_t = s13.find('<a:t>', s13.find('id="114"'))
idx_t_end = s13.find('</a:t>', idx_t)
if idx_t != -1:
    s13 = s13[:idx_t+5] + xml_escape("Justify the Design (3–5 minutes) – Architecture & Technology Justification") + s13[idx_t_end:]

idx_start = s13.find('<a:bodyPr', s13.find('id="115"'))
idx_end = s13.find('</p:txBody>', idx_start)
if idx_start != -1 and idx_end != -1:
    s13 = s13[:idx_start] + make_bullet_body(justification_items, "0284C7") + s13[idx_end:]

with open(s13_path, 'w', encoding='utf-8') as f:
    f.write(s13)
print("Updated Slide 13: Design Justification.")

# Pack the final presentation back into PPTX
with zipfile.ZipFile(output_pptx, 'w', zipfile.ZIP_DEFLATED) as z_out:
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, work_dir)
            z_out.write(full_path, rel_path)

print("SUCCESS: Generated complete PPTX at:", output_pptx)
