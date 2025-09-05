from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_login import login_required, current_user, logout_user
from FlaskMIS.models import Admins, Students
from Python_Part.Admin_class import Admin_class
from Python_Part.Student_class import Student_class

Main = Blueprint('Main', __name__)

@Main.route("/")
@Main.route("/home")
def home():
    return render_template("home_page.html")

@Main.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('Main.home'))

@Main.route('/student_performance')
@login_required
def student_performance():
    subject = request.args.get('subject')
    if isinstance(current_user, Admins):
        name = request.args.get('name')
        admin_per = Admin_class(subject)
        attempts_ad, percentage_ad = admin_per.get_subject_performance(name)
        if not attempts_ad:
            flash(f"No Record of {name} for {subject} subject.", "danger")
            return redirect(url_for("Admin.select_subject_name"))
        return render_template('student_performance.html',title ="Performance", student_name = name, selected_subject = subject, attempts = attempts_ad, percentage = percentage_ad)
    else:
        student_per = Student_class(subject)
        attempts_st, percentage_st = student_per.get_subject_performance(current_user.name)
        if not attempts_st:
            flash(f"No Record for {subject} subject.", "danger")
            return redirect(url_for("Main.select_subject"))
        return render_template('student_performance.html',title ="Performance", student_name = current_user.name, selected_subject = subject, attempts = attempts_st, percentage = percentage_st)
    
@Main.route('/select_subject', methods=['GET', 'POST'])
@login_required
def select_subject():
    option = request.args.get('option')
    if request.method == 'POST':
        selected_subject = request.form.get('subject')
        option = request.args.get('option')
        return redirect(url_for('Main.functionality', function_name = option, subject = selected_subject))
    return render_template('select_subject.html', option = option)
    
@Main.route("/functionality")
@login_required
def functionality():
    subject = request.args.get('subject')
    function_name = request.args.get('function_name')
    if isinstance(current_user, Students):
        if function_name == 'exam':
            return redirect(url_for('Student.number_que', subject = subject))
        else:
            return redirect(url_for('Main.student_performance', subject = subject))
    else:
        if function_name == 'view':
            return redirect(url_for('Admin.View_que', subject = subject))
        elif function_name == 'add':
            return redirect(url_for('Admin.Add_que', subject = subject))
        else:
            return redirect(url_for('Admin.Delete_que', subject = subject))