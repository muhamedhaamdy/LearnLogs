import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from learnlogs import app, db, bcrypt
from learnlogs.forms import EnrollForm, LoginForm, QuizForm, SubmibButton
from learnlogs.models import Student, Session, Student_Session
from flask_login import login_user, current_user, logout_user, login_required
from learnlogs.data import get_by_grade


'''
, UpdateAccountForm, PostForm
'''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/enroll", methods=['GET', 'POST'])
def enroll():
    # if current_user.  uthenticated:
    #     return redirect(url_for('home'))
    form = EnrollForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(
        student_name=form.student_name.data,
        email=form.email.data,
        password=hashed_password,
        student_phone=form.student_phone.data,
        parent_name=form.parent_name.data,
        parent_phone=form.parent_phone.data,
        address=form.address.data,
        photo_link=form.photo_link.data,
        grade=form.grade.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('enroll.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'teacher@elsheko.com' and form.password.data == '1234':
            return redirect(url_for('dashboard'))
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=False)
            return redirect(url_for('profile', id=student.id))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    student_first = len(Student.query.filter_by(grade='first').all())
    student_second = len(Student.query.filter_by(grade='second').all())
    student_third = len(Student.query.filter_by(grade='third').all())
    session_first = len(Session.query.filter_by(grade='first').all())
    session_second = len(Session.query.filter_by(grade='second').all())
    session_third = len(Session.query.filter_by(grade='third').all())
    return render_template('dashboard.html', student_first=student_first, 
                           student_second=student_second, student_third=student_third, session_first=session_first,
                            session_second=session_second, session_third=session_third)

@app.route('/dashboard/<string:grade>', methods=['GET', 'POST'])
def dashboard_grade(grade):
    all_data = get_by_grade(grade)
    students = Student.query.filter_by(grade=grade).all() 
    session = Session.query.filter_by(grade=grade).all()
    return render_template('dashboard_grade.html', all_students=all_data, students=students, sessions=session)

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    student = Student.query.filter_by(id=id).first()
    all_session = Session.query.filter_by(grade=student.grade).all()
    student_attended = sorted(student.attended, key=lambda session: session.id)
    student_marks = db.session.query(Student_Session).filter(Student_Session.c.student_id==id).order_by(Student_Session.c.session_id).all()
    if student:
        return render_template('student_profile.html', student=student,
                               marks=student_marks, attended=student_attended, sessions=all_session)

@app.route('/create_session/<string:grade>', methods=['GET', 'POST'])
def create_session(grade):
    forms = []
    button = SubmibButton()
    students = Student.query.filter_by(grade=grade).all()
    new_session = Session(grade=grade)
    db.session.add(new_session)
    db.session.commit()
    for student in students:
        form = QuizForm()
        forms.append((student, form))
    if request.method == 'POST':
        for student, form in forms:
            print(form.quiz_mark.data, button.quiz_full_mark.data)
            if button.validate_on_submit():
                student_session_entry = Student_Session.insert().values(student_id=student.id, 
                                                                  session_id=new_session.id, 
                                                                  mark=form.quiz_mark.data, 
                                                                  full_mark=button.quiz_full_mark.data)
                db.session.execute(student_session_entry)
                db.session.commit()
                return redirect(url_for('dashboard_grade', grade=grade))
        # return redirect(url_for('dashboard_grade', grade=grade))
    return render_template('create_session.html', form=forms, session=new_session, button=button)

""" 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
"""