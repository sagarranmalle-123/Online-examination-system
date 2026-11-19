import os, csv, io
from functools import wraps
from datetime import datetime, timezone
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, Response
)
from config import Config, BASE_DIR, get_db_uri
from models import db, User, Exam, Question, ExamResult, StudentAnswer

def create_app(config_class=Config):
    app = Flask(
        __name__,
        root_path=BASE_DIR,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )
    app.config.from_object(config_class)
    
    # Ensure environment variables are actively read at application instantiation
    runtime_secret = (os.environ.get('SECRET_KEY') or os.environ.get('FLASK_SECRET_KEY') or '').strip()
    if runtime_secret:
        app.config['SECRET_KEY'] = runtime_secret

    runtime_db = get_db_uri()
    if runtime_db:
        app.config['SQLALCHEMY_DATABASE_URI'] = runtime_db
    
    # Ensure instance directory exists safely (guard against read-only serverless filesystems)
    try:
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    except OSError:
        pass
    
    db.init_app(app)

    # Initialize tables automatically if they do not exist yet (NO demo-data seeding on startup)
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass
    
    # ================= AUTH HELPERS =================
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access admin desk.', 'warning')
                return redirect(url_for('login'))
            user = db.session.get(User, session['user_id'])
            if not user or not user.is_admin():
                flash('Access denied. Administrator privileges required.', 'danger')
                return redirect(url_for('student_dashboard'))
            return f(*args, **kwargs)
        return decorated_function

    @app.context_processor
    def inject_user():
        current_user = None
        if 'user_id' in session:
            current_user = db.session.get(User, session['user_id'])
        return dict(current_user=current_user)

    # ================= PUBLIC ROUTES =================
    @app.route('/')
    def index():
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                return redirect(url_for('admin_dashboard' if user.is_admin() else 'student_dashboard'))
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                return redirect(url_for('admin_dashboard' if user.is_admin() else 'student_dashboard'))

        if request.method == 'POST':
            identifier = request.form.get('identifier', '').strip()
            password = request.form.get('password', '')
            role = request.form.get('role', 'student')
            
            # Query user by email or roll_no
            user = User.query.filter(
                (User.email == identifier) | (User.roll_no == identifier)
            ).first()

            if user and user.check_password(password):
                if role == 'admin' and not user.is_admin():
                    flash('This account does not have administrator privileges.', 'danger')
                    return render_template('login.html', selected_role=role)
                
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_role'] = user.role
                flash(f'Welcome back, {user.name}!', 'success')
                
                if user.is_admin():
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid credentials. Please verify your email/roll number and password.', 'danger')

        role_query = request.args.get('role', 'student')
        return render_template('login.html', selected_role=role_query)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            roll_no = request.form.get('roll_no', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            department = request.form.get('department', 'Computer Science & Engineering')
            semester = request.form.get('semester', '4th Semester')

            if password != confirm_password:
                flash('Passwords do not match. Please re-enter.', 'danger')
                return render_template('register.html')

            if User.query.filter_by(email=email).first():
                flash('An account with this email address already exists.', 'warning')
                return render_template('register.html')

            if roll_no and User.query.filter_by(roll_no=roll_no).first():
                flash('An account with this Roll Number / PRN already exists.', 'warning')
                return render_template('register.html')

            new_user = User(
                name=name,
                roll_no=roll_no,
                email=email,
                role='student',
                department=department,
                semester=semester
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in with your credentials.', 'success')
            return redirect(url_for('login', role='student'))

        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out securely.', 'info')
        return redirect(url_for('index'))

    # ================= STUDENT MODULES =================
    @app.route('/student/dashboard')
    @login_required
    def student_dashboard():
        user = db.session.get(User, session['user_id'])
        if user.is_admin():
            return redirect(url_for('admin_dashboard'))

        # Fetch active exams
        exams = Exam.query.filter_by(is_active=True).order_by(Exam.created_at.desc()).all()
        
        # Fetch user results mapping
        results = ExamResult.query.filter_by(user_id=user.id).all()
        results_map = {r.exam_id: r for r in results}

        # Compute summary metrics
        total_attempted = len(results)
        passed_count = sum(1 for r in results if r.passed)
        avg_percentage = round(sum(r.percentage for r in results) / total_attempted, 1) if total_attempted > 0 else 0.0

        return render_template(
            'student_dashboard.html',
            user=user,
            exams=exams,
            results_map=results_map,
            total_attempted=total_attempted,
            passed_count=passed_count,
            avg_percentage=avg_percentage
        )

    @app.route('/exam/<int:exam_id>/instructions')
    @login_required
    def exam_instructions(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        user = db.session.get(User, session['user_id'])
        
        # Check if already attempted
        existing_result = ExamResult.query.filter_by(user_id=user.id, exam_id=exam.id).first()
        if existing_result:
            flash(f'You have already completed this exam on {existing_result.submitted_at.strftime("%d-%b-%Y")}.', 'info')
            return redirect(url_for('result_detail', result_id=existing_result.id))

        return render_template('exam_instructions.html', exam=exam, user=user)

    @app.route('/exam/<int:exam_id>/start')
    @login_required
    def start_exam(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        user = db.session.get(User, session['user_id'])

        # Disallow re-attempting if result exists
        existing_result = ExamResult.query.filter_by(user_id=user.id, exam_id=exam.id).first()
        if existing_result:
            flash('Exam already submitted. You cannot re-take this assessment.', 'warning')
            return redirect(url_for('result_detail', result_id=existing_result.id))

        questions = Question.query.filter_by(exam_id=exam.id).all()
        if not questions:
            flash('This exam currently has no questions configured. Please contact faculty.', 'warning')
            return redirect(url_for('student_dashboard'))

        # Pack safe questions without exposing answer keys
        safe_questions = [q.to_dict() for q in questions]

        return render_template(
            'exam_screen.html',
            exam=exam,
            user=user,
            questions_json=safe_questions,
            total_questions=len(questions)
        )

    @app.route('/api/exam/<int:exam_id>/submit', methods=['POST'])
    @login_required
    def submit_exam_api(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        user = db.session.get(User, session['user_id'])

        # Check existing result to prevent duplicate submissions
        existing_result = ExamResult.query.filter_by(user_id=user.id, exam_id=exam.id).first()
        if existing_result:
            return jsonify({'success': False, 'message': 'Exam already submitted', 'result_id': existing_result.id}), 400

        data = request.get_json() or {}
        submitted_answers = data.get('answers', {})  # str(q_id) -> 'A'/'B'/'C'/'D'
        time_taken = data.get('time_taken_seconds', 0)
        strike_count = data.get('strike_count', 0)

        questions = Question.query.filter_by(exam_id=exam.id).all()
        
        score = 0.0
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0

        # Calculate max possible score
        max_score = sum(q.marks for q in questions) if questions else exam.total_marks

        # Create base ExamResult record
        result = ExamResult(
            user_id=user.id,
            exam_id=exam.id,
            score=0.0,
            max_score=max_score,
            percentage=0.0,
            passed=False,
            total_questions=len(questions),
            correct_count=0,
            incorrect_count=0,
            unanswered_count=0,
            time_taken_seconds=time_taken,
            strike_count=strike_count,
            submitted_at=datetime.now(timezone.utc)
        )
        db.session.add(result)
        db.session.flush()  # assign result.id

        # Grade each question atomically
        for q in questions:
            selected_opt = submitted_answers.get(str(q.id))
            is_correct = False
            marks_awarded = 0.0

            if not selected_opt:
                unanswered_count += 1
            elif selected_opt.upper() == q.correct_option.upper():
                is_correct = True
                marks_awarded = q.marks
                correct_count += 1
                score += marks_awarded
            else:
                incorrect_count += 1
                # Deduct negative marks if configured
                neg = exam.negative_marks_per_q if exam.negative_marks_per_q else 0.0
                marks_awarded = -neg
                score -= neg

            ans_record = StudentAnswer(
                result_id=result.id,
                question_id=q.id,
                selected_option=selected_opt.upper() if selected_opt else None,
                is_correct=is_correct,
                marks_awarded=marks_awarded
            )
            db.session.add(ans_record)

        # Floor score at 0.0
        final_score = round(max(0.0, score), 2)
        percentage = round((final_score / max_score) * 100, 1) if max_score > 0 else 0.0
        passed = final_score >= exam.passing_marks

        result.score = final_score
        result.percentage = percentage
        result.passed = passed
        result.correct_count = correct_count
        result.incorrect_count = incorrect_count
        result.unanswered_count = unanswered_count

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Exam submitted and evaluated successfully!',
            'result_id': result.id
        })

    @app.route('/result/<int:result_id>')
    @login_required
    def result_detail(result_id):
        result = db.get_or_404(ExamResult, result_id)
        current_u = db.session.get(User, session['user_id'])

        # Security check: only the student who took it or an admin can view
        if not current_u.is_admin() and result.user_id != current_u.id:
            flash('Access unauthorized.', 'danger')
            return redirect(url_for('student_dashboard'))

        # Fetch answers paired with questions
        answers_data = []
        for ans in result.answers:
            q = db.session.get(Question, ans.question_id)
            answers_data.append({
                'question': q,
                'selected_option': ans.selected_option,
                'is_correct': ans.is_correct,
                'marks_awarded': ans.marks_awarded
            })

        # Calculate rank among all examinees of this exam
        all_exam_results = ExamResult.query.filter_by(exam_id=result.exam_id).order_by(ExamResult.score.desc()).all()
        rank = 1
        for idx, r in enumerate(all_exam_results):
            if r.id == result.id:
                rank = idx + 1
                break

        return render_template(
            'result_detail.html',
            result=result,
            exam=result.exam,
            student=result.student,
            answers_data=answers_data,
            rank=rank,
            total_candidates=len(all_exam_results)
        )

    @app.route('/student/history')
    @login_required
    def student_history():
        user = db.session.get(User, session['user_id'])
        results = ExamResult.query.filter_by(user_id=user.id).order_by(ExamResult.submitted_at.desc()).all()
        return render_template('student_history.html', user=user, results=results)

    # ================= ADMIN MODULES =================
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        total_students = User.query.filter_by(role='student').count()
        total_exams = Exam.query.count()
        total_questions = Question.query.count()
        total_submissions = ExamResult.query.count()
        
        all_results = ExamResult.query.all()
        avg_score = round(sum(r.percentage for r in all_results) / len(all_results), 1) if all_results else 0.0

        recent_submissions = ExamResult.query.order_by(ExamResult.submitted_at.desc()).limit(8).all()
        exams = Exam.query.order_by(Exam.created_at.desc()).all()

        return render_template(
            'admin_dashboard.html',
            total_students=total_students,
            total_exams=total_exams,
            total_questions=total_questions,
            total_submissions=total_submissions,
            avg_score=avg_score,
            recent_submissions=recent_submissions,
            exams=exams
        )

    @app.route('/admin/exams')
    @admin_required
    def admin_exams():
        exams = Exam.query.order_by(Exam.created_at.desc()).all()
        return render_template('admin_exams.html', exams=exams)

    @app.route('/admin/exams/create', methods=['GET', 'POST'])
    @admin_required
    def admin_create_exam():
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            course_code = request.form.get('course_code', '').strip().upper()
            description = request.form.get('description', '').strip()
            duration_minutes = int(request.form.get('duration_minutes', 60))
            total_marks = float(request.form.get('total_marks', 50))
            passing_marks = float(request.form.get('passing_marks', 20))
            negative_marks = float(request.form.get('negative_marks_per_q', 0.25))
            is_active = True if request.form.get('is_active') else False

            exam = Exam(
                title=title,
                course_code=course_code,
                description=description,
                duration_minutes=duration_minutes,
                total_marks=total_marks,
                passing_marks=passing_marks,
                negative_marks_per_q=negative_marks,
                is_active=is_active,
                created_by_id=session['user_id']
            )
            db.session.add(exam)
            db.session.commit()

            flash(f'Examination "{exam.course_code}: {exam.title}" created successfully! Now author questions for this exam.', 'success')
            return redirect(url_for('admin_exam_questions', exam_id=exam.id))

        return render_template('admin_exam_form.html', exam=None)

    @app.route('/admin/exams/<int:exam_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_exam(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        if request.method == 'POST':
            exam.title = request.form.get('title', '').strip()
            exam.course_code = request.form.get('course_code', '').strip().upper()
            exam.description = request.form.get('description', '').strip()
            exam.duration_minutes = int(request.form.get('duration_minutes', 60))
            exam.total_marks = float(request.form.get('total_marks', 50))
            exam.passing_marks = float(request.form.get('passing_marks', 20))
            exam.negative_marks_per_q = float(request.form.get('negative_marks_per_q', 0.25))
            exam.is_active = True if request.form.get('is_active') else False

            db.session.commit()
            flash('Examination settings updated successfully!', 'success')
            return redirect(url_for('admin_exams'))

        return render_template('admin_exam_form.html', exam=exam)

    @app.route('/admin/exams/<int:exam_id>/toggle')
    @admin_required
    def admin_toggle_exam(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        exam.is_active = not exam.is_active
        db.session.commit()
        status_str = "Published & Live" if exam.is_active else "Draft / Inactive"
        flash(f'Exam "{exam.course_code}" status changed to: {status_str}', 'info')
        return redirect(url_for('admin_exams'))

    @app.route('/admin/exams/<int:exam_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_exam(exam_id):
        exam = db.get_or_404(Exam, exam_id)
        title = exam.title
        db.session.delete(exam)
        db.session.commit()
        flash(f'Exam "{title}" and associated questions/results deleted.', 'warning')
        return redirect(url_for('admin_exams'))

    @app.route('/admin/exams/<int:exam_id>/questions', methods=['GET', 'POST'])
    @admin_required
    def admin_exam_questions(exam_id):
        exam = db.get_or_404(Exam, exam_id)

        if request.method == 'POST':
            question_text = request.form.get('question_text', '').strip()
            option_a = request.form.get('option_a', '').strip()
            option_b = request.form.get('option_b', '').strip()
            option_c = request.form.get('option_c', '').strip()
            option_d = request.form.get('option_d', '').strip()
            correct_option = request.form.get('correct_option', 'A').strip().upper()
            marks = float(request.form.get('marks', 2.0))
            explanation = request.form.get('explanation', '').strip()
            difficulty = request.form.get('difficulty', 'Medium')

            q = Question(
                exam_id=exam.id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
                marks=marks,
                explanation=explanation,
                difficulty=difficulty
            )
            db.session.add(q)
            db.session.commit()
            flash('Question added to Question Bank!', 'success')
            return redirect(url_for('admin_exam_questions', exam_id=exam.id))

        questions = Question.query.filter_by(exam_id=exam.id).all()
        return render_template('admin_questions.html', exam=exam, questions=questions)

    @app.route('/admin/questions/<int:question_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_question(question_id):
        q = db.get_or_404(Question, question_id)
        exam_id = q.exam_id
        db.session.delete(q)
        db.session.commit()
        flash('Question removed from Question Bank.', 'info')
        return redirect(url_for('admin_exam_questions', exam_id=exam_id))

    @app.route('/admin/questions/<int:question_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_question(question_id):
        q = db.get_or_404(Question, question_id)
        exam = q.exam
        if request.method == 'POST':
            q.question_text = request.form.get('question_text', '').strip()
            q.option_a = request.form.get('option_a', '').strip()
            q.option_b = request.form.get('option_b', '').strip()
            q.option_c = request.form.get('option_c', '').strip()
            q.option_d = request.form.get('option_d', '').strip()
            q.correct_option = request.form.get('correct_option', 'A').strip().upper()
            q.marks = float(request.form.get('marks', 2.0))
            q.explanation = request.form.get('explanation', '').strip()
            q.difficulty = request.form.get('difficulty', 'Medium')
            db.session.commit()
            flash('Question updated successfully!', 'success')
            return redirect(url_for('admin_exam_questions', exam_id=exam.id))
        return render_template('admin_question_edit.html', exam=exam, question=q)

    @app.route('/admin/students')
    @admin_required
    def admin_students():
        students = User.query.filter_by(role='student').order_by(User.name.asc()).all()
        return render_template('admin_students.html', students=students)

    @app.route('/admin/students/<int:student_id>/delete', methods=['POST'])
    @admin_required
    def admin_delete_student(student_id):
        student = db.get_or_404(User, student_id)
        if student.is_admin():
            flash('Administrator accounts cannot be deleted here.', 'danger')
            return redirect(url_for('admin_students'))
        name = student.name
        db.session.delete(student)
        db.session.commit()
        flash(f'Student "{name}" and all associated records removed successfully.', 'info')
        return redirect(url_for('admin_students'))

    @app.route('/admin/results')
    @admin_required
    def admin_results():
        exam_filter = request.args.get('exam_id', type=int)
        student_filter = request.args.get('student_id', type=int)
        query = ExamResult.query
        if exam_filter:
            query = query.filter_by(exam_id=exam_filter)
        if student_filter:
            query = query.filter_by(user_id=student_filter)
        
        results = query.order_by(ExamResult.submitted_at.desc()).all()
        exams = Exam.query.all()

        return render_template(
            'admin_results.html',
            results=results,
            exams=exams,
            selected_exam=exam_filter
        )

    @app.route('/admin/results/export')
    @admin_required
    def admin_export_results_csv():
        results = ExamResult.query.order_by(ExamResult.submitted_at.desc()).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Result ID', 'Student Name', 'Roll Number', 'Email',
            'Course Code', 'Exam Title', 'Score', 'Max Score',
            'Percentage', 'Status', 'Correct', 'Incorrect', 'Unanswered',
            'Time Taken (Sec)', 'Strikes Logged', 'Submission Timestamp'
        ])

        for r in results:
            writer.writerow([
                r.id, r.student.name, r.student.roll_no or 'N/A', r.student.email,
                r.exam.course_code, r.exam.title, r.score, r.max_score,
                f"{r.percentage}%", "PASSED" if r.passed else "FAILED",
                r.correct_count, r.incorrect_count, r.unanswered_count,
                r.time_taken_seconds, r.strike_count, r.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=Presidency_Exam_Results.csv"}
        )

    return app

# Expose app variable at root level for Vercel, WSGI, and deployment platforms
app = create_app()

@app.cli.command('seed-db')
def seed_db():
    """Seed the database with initial users, courses, and question banks."""
    from seed_data import seed_database
    seed_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)

