from flask import render_template, flash, redirect, url_for, Blueprint, session, request
from FlaskMIS.Student.Forms import RegistrationForm, LoginForm
from FlaskMIS import db, bcrypt
from FlaskMIS.models import Admins, Students
from flask_login import login_user, current_user, login_required
from Python_Part.Student_class import Student_class
import json
Student = Blueprint('Student', __name__)


@Student.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if isinstance(current_user, Admins):
            return redirect(url_for('Admin.admin'))
        else:
            return redirect(url_for('Student.student'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Students(name = form.name.data, username=form.username.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash(f"Account Successfully Created for {form.name.data}!", 'success')
        return redirect(url_for('Student.login_student'))
    return render_template("register.html", title="Register", form=form)

@Student.route("/login_student", methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        if isinstance(current_user, Admins):
            return redirect(url_for('Admin.admin'))
        else:
            return redirect(url_for('Student.student'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(username=form.username.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=False)
            session['user_role'] = 'student'
            return redirect(url_for('Student.student'))
        else:
            flash("Login Unsuccessful. Check Username and Password", 'danger')
    return render_template("login_student.html", title="Student Login", form=form)


@Student.route("/student")
@login_required
def student():
    if isinstance(current_user, Admins):  # If an admin tries to access student page
        flash("Access Denied! Redirecting to Admin Dashboard.", "danger")
        return redirect(url_for("Admin.admin"))  # Redirect them to admin dashboard
    return render_template("student.html", title="Student")

@Student.route("/number_que", methods=['GET', 'POST'])
@login_required
def number_que():
    if isinstance(current_user, Admins):
        flash("Access Denied! Redirecting to Admin Dashboard.", "danger")
        return redirect(url_for("Admin.admin"))
    else:
        subject = request.args.get('subject')
        if request.method == 'POST':
            subject = request.args.get('subject')
            number = int(request.form.get('num_questions'))
            student_exam = Student_class(subject)
            questions = student_exam.get_question_from_number(number)
            session['subject'] = json.dumps(subject)
            session['questions'] = json.dumps(questions)
            is_correct = []
            session['is_correct'] = json.dumps(is_correct)
            return redirect(url_for('Student.Exam_que',qid = 0, is_correct = is_correct))
        student_max_number = Student_class(subject)
        max_number = student_max_number.get_max_question()
        return render_template("number_que.html", subject = subject, max_number = max_number)

@Student.route("/Exam_que/<int:qid>", methods=['GET', 'POST'])
@login_required
def Exam_que(qid):
    if isinstance(current_user, Admins):
        flash("Access Denied! Redirecting to Admin Dashboard.", "danger")
        return redirect(url_for("Admin.admin"))
    else:
        questions = json.loads(session.get('questions'))
        if request.method == 'POST':
            selected_option = request.form.get('selected_option')
            questions = json.loads(session.get('questions'))
            correct_answer = questions[qid - 1][5]
            is_correct = json.loads(session.get('is_correct'))
            if selected_option == correct_answer:
                is_correct.append([questions[qid - 1][0],1,selected_option])
            else:
                is_correct.append([questions[qid - 1][0],0,selected_option,correct_answer])
            session['is_correct'] = json.dumps(is_correct)

        if qid >= len(questions):
            return redirect(url_for('Student.result_after_exam'))

        current_question = questions[qid]
        return render_template(
            'Exam_que.html',
            qid=qid,
            question_text=current_question[0],
            options=current_question[1:5]
        )
    
@Student.route("/result_after_exam")
@login_required
def result_after_exam():
    if isinstance(current_user, Admins):  # If an admin tries to access student page
        flash("Access Denied! Redirecting to Admin Dashboard.", "danger")
        return redirect(url_for("Admin.admin"))  # Redirect them to admin dashboard
    else:
        session.pop('questions', None)
        is_correct = json.loads(session.get('is_correct', '[]'))
        session.pop('is_correct', None)

        total_questions = len(is_correct)
        correct_answers = sum(1 for item in is_correct if item[1] == 1)
        percentage = (correct_answers / total_questions) * 100

        subject = json.loads(session.get('subject'))
        session.pop('subject', None)
        student_result = Student_class(subject)
        student_result.set_result(current_user.name, percentage)
        return render_template('result_after_exam.html', results=is_correct, percentage = percentage)