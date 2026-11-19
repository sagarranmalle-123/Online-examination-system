import unittest
import json
from app import create_app
from models import db, User, Exam, Question, ExamResult, StudentAnswer

class OnlineExaminationSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed test admin
        self.admin = User(
            name="Admin Faculty",
            email="admin@test.edu",
            role="admin",
            department="Computer Science"
        )
        self.admin.set_password("Admin@123")
        db.session.add(self.admin)

        # Seed test student
        self.student = User(
            name="Student One",
            roll_no="20241CSE0001",
            email="student@test.edu",
            role="student",
            department="Computer Science",
            semester="4th Semester"
        )
        self.student.set_password("Student@123")
        db.session.add(self.student)

        # Seed second test student for privacy check
        self.student2 = User(
            name="Student Two",
            roll_no="20241CSE0002",
            email="student2@test.edu",
            role="student",
            department="Computer Science",
            semester="4th Semester"
        )
        self.student2.set_password("Student@123")
        db.session.add(self.student2)

        # Seed test exam with negative marking
        self.exam = Exam(
            title="Software Engineering Principles",
            course_code="CSE2271",
            description="Unit Testing and Software Architecture Exam",
            duration_minutes=30,
            total_marks=20.0,
            passing_marks=8.0,
            negative_marks_per_q=0.5,
            is_active=True,
            created_by_id=self.admin.id
        )
        db.session.add(self.exam)
        db.session.commit()

        # Seed 3 questions
        self.q1 = Question(
            exam_id=self.exam.id,
            question_text="What does MVC stand for?",
            option_a="Model View Controller",
            option_b="Multi View Computer",
            option_c="Model Video Core",
            option_d="Main Value Control",
            correct_option="A",
            marks=4.0,
            explanation="MVC separates concerns into Model, View, and Controller.",
            difficulty="Easy"
        )
        self.q2 = Question(
            exam_id=self.exam.id,
            question_text="Which database property guarantees transactions are all-or-nothing?",
            option_a="Consistency",
            option_b="Atomicity",
            option_c="Isolation",
            option_d="Durability",
            correct_option="B",
            marks=4.0,
            explanation="Atomicity ensures either all operations succeed or none.",
            difficulty="Medium"
        )
        self.q3 = Question(
            exam_id=self.exam.id,
            question_text="What is the worst-case complexity of binary search?",
            option_a="O(N)",
            option_b="O(1)",
            option_c="O(log N)",
            option_d="O(N^2)",
            correct_option="C",
            marks=4.0,
            explanation="Binary search repeatedly halves the search space.",
            difficulty="Medium"
        )
        db.session.add_all([self.q1, self.q2, self.q3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 1. Models & Cryptography
    def test_user_password_hashing(self):
        user = User.query.filter_by(email="student@test.edu").first()
        self.assertTrue(user.check_password("Student@123"))
        self.assertFalse(user.check_password("WrongPassword"))
        self.assertNotEqual(user.password_hash, "Student@123")

    # 2. Registration Flow
    def test_student_registration_success(self):
        response = self.client.post('/register', data={
            'name': 'New Student',
            'roll_no': '20241CSE0999',
            'email': 'newstudent@test.edu',
            'password': 'Password@123',
            'confirm_password': 'Password@123',
            'department': 'Computer Science & Engineering',
            'semester': '4th Semester'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='newstudent@test.edu').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.roll_no, '20241CSE0999')

    def test_registration_validation_duplicate_email(self):
        response = self.client.post('/register', data={
            'name': 'Duplicate Email',
            'roll_no': '20241CSE0888',
            'email': 'student@test.edu',  # already exists
            'password': 'Password@123',
            'confirm_password': 'Password@123',
            'department': 'CSE',
            'semester': '4th'
        }, follow_redirects=True)
        self.assertIn(b'An account with this email address already exists', response.data)

    def test_registration_validation_password_mismatch(self):
        response = self.client.post('/register', data={
            'name': 'Mismatch Student',
            'roll_no': '20241CSE0777',
            'email': 'mismatch@test.edu',
            'password': 'Password@123',
            'confirm_password': 'Password@999',
            'department': 'CSE',
            'semester': '4th'
        }, follow_redirects=True)
        self.assertIn(b'Passwords do not match', response.data)

    # 3. Authentication & RBAC
    def test_student_login_and_logout(self):
        # Login
        response = self.client.post('/login', data={
            'identifier': 'student@test.edu',
            'password': 'Student@123',
            'role': 'student'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, Student One', response.data)

        # Logout
        resp_logout = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out securely', resp_logout.data)

    def test_admin_desk_security_barrier(self):
        # As student, attempting to access admin dashboard must be denied
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.student.id
            sess['user_role'] = 'student'

        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Access denied. Administrator privileges required', response.data)

    # 4. Admin Management Operations
    def test_admin_exam_crud(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.admin.id
            sess['user_role'] = 'admin'

        # Create Exam
        create_resp = self.client.post('/admin/exams/create', data={
            'title': 'Operating Systems & Concurrency',
            'course_code': 'CSE2300',
            'description': 'Process scheduling, threads, virtual memory',
            'duration_minutes': '45',
            'total_marks': '30.0',
            'passing_marks': '12.0',
            'negative_marks_per_q': '0.5',
            'is_active': 'y'
        }, follow_redirects=True)
        self.assertEqual(create_resp.status_code, 200)
        new_exam = Exam.query.filter_by(course_code='CSE2300').first()
        self.assertIsNotNone(new_exam)

        # Edit Exam
        edit_resp = self.client.post(f'/admin/exams/{new_exam.id}/edit', data={
            'title': 'Operating Systems Advanced',
            'course_code': 'CSE2300',
            'description': 'Updated description',
            'duration_minutes': '50',
            'total_marks': '40.0',
            'passing_marks': '16.0',
            'negative_marks_per_q': '0.25',
            'is_active': 'y'
        }, follow_redirects=True)
        self.assertEqual(edit_resp.status_code, 200)
        self.assertEqual(new_exam.duration_minutes, 50)

        # Toggle Exam Active Status
        toggle_resp = self.client.get(f'/admin/exams/{new_exam.id}/toggle', follow_redirects=True)
        self.assertFalse(new_exam.is_active)

        # Delete Exam
        del_resp = self.client.post(f'/admin/exams/{new_exam.id}/delete', follow_redirects=True)
        self.assertIsNone(db.session.get(Exam, new_exam.id))

    def test_admin_question_authoring_and_editing(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.admin.id
            sess['user_role'] = 'admin'

        # Add Question
        add_resp = self.client.post(f'/admin/exams/{self.exam.id}/questions', data={
            'question_text': 'What is a deadlock condition in OS?',
            'option_a': 'Mutual Exclusion',
            'option_b': 'Hold and Wait',
            'option_c': 'No Preemption',
            'option_d': 'All of the above',
            'correct_option': 'D',
            'marks': '3.0',
            'explanation': 'Coffman conditions include mutual exclusion, hold and wait, no preemption, circular wait.',
            'difficulty': 'Medium'
        }, follow_redirects=True)
        self.assertIn(b'Question added to Question Bank', add_resp.data)
        new_q = Question.query.filter_by(question_text='What is a deadlock condition in OS?').first()
        self.assertIsNotNone(new_q)

        # Edit Question
        edit_resp = self.client.post(f'/admin/questions/{new_q.id}/edit', data={
            'question_text': 'What are the 4 Coffman deadlock conditions in OS?',
            'option_a': 'Mutual Exclusion',
            'option_b': 'Hold and Wait',
            'option_c': 'No Preemption',
            'option_d': 'All 4 conditions required',
            'correct_option': 'D',
            'marks': '4.0',
            'explanation': 'All 4 Coffman conditions must hold simultaneously for a deadlock.',
            'difficulty': 'Hard'
        }, follow_redirects=True)
        self.assertIn(b'Question updated successfully', edit_resp.data)
        self.assertEqual(new_q.marks, 4.0)

        # Delete Question
        del_resp = self.client.post(f'/admin/questions/{new_q.id}/delete', follow_redirects=True)
        self.assertIsNone(db.session.get(Question, new_q.id))

    def test_admin_student_directory_and_management(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.admin.id
            sess['user_role'] = 'admin'

        # View Students
        resp = self.client.get('/admin/students')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Registered Students Directory', resp.data)
        self.assertIn(b'20241CSE0001', resp.data)

        # Remove Student
        del_resp = self.client.post(f'/admin/students/{self.student2.id}/delete', follow_redirects=True)
        self.assertIn(b'removed successfully', del_resp.data)
        self.assertIsNone(db.session.get(User, self.student2.id))

    # 5. Live Test & Automatic Server-Side Grading
    def test_exam_start_payload_security(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.student.id
            sess['user_role'] = 'student'

        resp = self.client.get(f'/exam/{self.exam.id}/start')
        self.assertEqual(resp.status_code, 200)
        # Verify master answer key and explanation are NOT leaked in student screen
        # to_dict() only serializes id, question_text, options, marks, difficulty
        self.assertNotIn(b'"correct_option"', resp.data)

    def test_exam_submission_and_automatic_evaluation(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.student.id
            sess['user_role'] = 'student'

        # Submit answers:
        # q1: correct ('A') -> +4.0 marks
        # q2: incorrect ('A' instead of 'B') -> -0.5 marks negative penalty
        # q3: unanswered -> 0.0 marks
        # Total expected: 4.0 - 0.5 = 3.5 marks out of 12.0 (29.2%), Failed (cutoff is 8.0)
        payload = {
            'answers': {
                str(self.q1.id): 'A',
                str(self.q2.id): 'A',
                # q3 omitted
            },
            'time_taken_seconds': 420,
            'strike_count': 1
        }

        resp = self.client.post(
            f'/api/exam/{self.exam.id}/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        result_id = data['result_id']

        result = db.session.get(ExamResult, result_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.score, 3.5)
        self.assertEqual(result.correct_count, 1)
        self.assertEqual(result.incorrect_count, 1)
        self.assertEqual(result.unanswered_count, 1)
        self.assertFalse(result.passed)
        self.assertEqual(result.strike_count, 1)
        self.assertEqual(result.time_taken_seconds, 420)

        # 6. Disallow Duplicate Exam Submission
        dup_resp = self.client.post(
            f'/api/exam/{self.exam.id}/submit',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(dup_resp.status_code, 400)
        dup_data = dup_resp.get_json()
        self.assertFalse(dup_data['success'])

        # 7. Disallow Re-taking via start route
        start_attempt = self.client.get(f'/exam/{self.exam.id}/start', follow_redirects=True)
        self.assertIn(b'Exam already submitted', start_attempt.data)

        # 8. Student Scorecard View
        scorecard_resp = self.client.get(f'/result/{result.id}')
        self.assertEqual(scorecard_resp.status_code, 200)
        self.assertIn(b'Official Examination Scorecard', scorecard_resp.data)

        # 9. Privacy check: Student 2 cannot view Student 1's result
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.student2.id
            sess['user_role'] = 'student'

        unauth_resp = self.client.get(f'/result/{result.id}', follow_redirects=True)
        self.assertIn(b'Access unauthorized', unauth_resp.data)

    # 10. Admin CSV Export
    def test_admin_csv_export(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.admin.id
            sess['user_role'] = 'admin'

        csv_resp = self.client.get('/admin/results/export')
        self.assertEqual(csv_resp.status_code, 200)
        self.assertEqual(csv_resp.mimetype, 'text/csv')
        self.assertIn(b'Result ID,Student Name,Roll Number,Email', csv_resp.data)

if __name__ == '__main__':
    unittest.main()
