from flask import Blueprint, session, request
from flask import render_template, flash, redirect, url_for
from FlaskMIS.Student.Forms import LoginForm
from FlaskMIS import bcrypt
from FlaskMIS.models import Admins, Students
from flask_login import login_user, current_user, login_required
from Python_Part.Admin_class import Admin_class

Admin = Blueprint('Admin', __name__)

@Admin.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        if isinstance(current_user, Admins):
            return redirect(url_for('Admin.admin'))
        else:
            return redirect(url_for('Student.student'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admins.query.filter_by(username=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=False)
            session['user_role'] = 'admin'
            return redirect(url_for('Admin.admin'))
        else:
            flash("Login Unsuccessful. Check Username and Password", 'danger')
    return render_template("login_admin.html", title="Admin Login", form=form)

@Admin.route("/admin")
@login_required
def admin():
    if isinstance(current_user, Students):  # If a student tries to access admin page
        flash("Access Denied! Redirecting to Student Dashboard.", "danger")
        return redirect(url_for("Student.student"))  # Redirect them to student dashboard
    return render_template("admin.html", title="Admin")

@Admin.route('/select_subject_name', methods=['GET', 'POST'])
@login_required
def select_subject_name():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        selected_subject = request.form.get('subject')
        return redirect(url_for('Main.student_performance', name = student_name, subject = selected_subject))
    return render_template('select_subject_name.html')

@Admin.route("/View_que")
@login_required
def View_que():
    if isinstance(current_user, Students):  # If a student tries to access View_que page
        flash("Access Denied! Redirecting to Student Dashboard.", "danger")
        return redirect(url_for("Student.student"))  # Redirect them to student dashboard
    else:
        subject = request.args.get('subject')
        admin_view = Admin_class(subject)
        questions = admin_view.View_que()
        return render_template("View_que.html", title="View Question", questions = questions)

@Admin.route("/Add_que", methods=['GET', 'POST'])
@login_required
def Add_que():
    if isinstance(current_user, Students):  # If a student tries to access Add_que page
        flash("Access Denied! Redirecting to Student Dashboard.", "danger")
        return redirect(url_for("Student.student"))  # Redirect them to student dashboard
    else:
        subject = request.args.get('subject')
        if request.method == 'POST':
            subject = request.args.get('subject')
            question = request.form.get('question')
            option1 = request.form.get('option1')
            option2 = request.form.get('option2')
            option3 = request.form.get('option3')
            option4 = request.form.get('option4')
            ans = request.form.get('correct_answer')
            admin_add = Admin_class(subject)
            admin_add.AddQA(question, option1, option2, option3, option4, ans)
            flash("Question added Successfully", 'success')
            return redirect(url_for('Admin.admin'))
        return render_template("Add_que.html", title="Add Question", subject = subject)

@Admin.route("/Delete_que", methods=['GET', 'POST'])
@login_required
def Delete_que():
    if isinstance(current_user, Students):  # If a student tries to access Delete_que page
        flash("Access Denied! Redirecting to Student Dashboard.", "danger")
        return redirect(url_for("Student.student"))  # Redirect them to student dashboard
    else:
        subject = request.args.get('subject')
        admin_view = Admin_class(subject)
        questions = admin_view.View_que()
        if request.method == 'POST':
            to_delete = request.form['question']
            subject = request.args.get('subject')
            admin_view2 = Admin_class(subject)
            admin_view2.Delete_QA(to_delete)
            return redirect(url_for('Admin.admin'))
    
        return render_template('Delete_que.html',title ="Delete Question", questions=questions)
