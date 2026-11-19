from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'admin'
    department = db.Column(db.String(100), default='Computer Science and Engineering')
    semester = db.Column(db.String(20), default='4th Semester')
    created_at = db.Column(db.DateTime, default=utc_now)
    
    # Relationships
    results = db.relationship('ExamResult', backref='student', lazy=True, cascade='all, delete-orphan')
    exams_created = db.relationship('Exam', backref='creator', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    total_marks = db.Column(db.Float, nullable=False, default=50.0)
    passing_marks = db.Column(db.Float, nullable=False, default=20.0)
    negative_marks_per_q = db.Column(db.Float, nullable=False, default=0.25)
    is_active = db.Column(db.Boolean, default=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    
    # Relationships
    questions = db.relationship('Question', backref='exam', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('ExamResult', backref='exam', lazy=True, cascade='all, delete-orphan')
    
    def question_count(self):
        return len(self.questions)

    def __repr__(self):
        return f'<Exam {self.course_code}: {self.title}>'


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    marks = db.Column(db.Float, nullable=False, default=2.0)
    explanation = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), default='Medium')
    
    # Relationships
    answers = db.relationship('StudentAnswer', backref='question', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'marks': self.marks,
            'difficulty': self.difficulty
            # Do NOT expose correct_option or explanation in student test stream!
        }


class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False)
    incorrect_count = db.Column(db.Integer, nullable=False)
    unanswered_count = db.Column(db.Integer, nullable=False)
    time_taken_seconds = db.Column(db.Integer, default=0)
    strike_count = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=utc_now)
    
    # Relationships
    answers = db.relationship('StudentAnswer', backref='result', lazy=True, cascade='all, delete-orphan')

    def formatted_time(self):
        mins = self.time_taken_seconds // 60
        secs = self.time_taken_seconds % 60
        return f"{mins}m {secs}s"


class StudentAnswer(db.Model):
    __tablename__ = 'student_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('exam_results.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=True)  # 'A', 'B', 'C', 'D' or None
    is_correct = db.Column(db.Boolean, default=False)
    marks_awarded = db.Column(db.Float, default=0.0)

