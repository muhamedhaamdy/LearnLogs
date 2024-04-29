import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from learnlogs import app, db, bcrypt
from learnlogs.forms import EnrollForm, LoginForm, Submit_Student_mark, SessionForm
from learnlogs.models import Student, Session, Student_Session
from flask_login import login_user, current_user, logout_user, login_required
from learnlogs.data import get_by_grade


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
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
            login_user(Student.query.filter_by(email='teacher@elsheko.com').first(), remember=False)
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
    if current_user.is_authenticated:
        if current_user.email==('teacher@elsheko.com'):
            student_first = len(Student.query.filter_by(grade='first').all())
            student_second = len(Student.query.filter_by(grade='second').all())
            student_third = len(Student.query.filter_by(grade='third').all())
            session_first = len(Session.query.filter_by(grade='first').all())
            session_second = len(Session.query.filter_by(grade='second').all())
            session_third = len(Session.query.filter_by(grade='third').all())
            return render_template('dashboard.html', student_first=student_first, 
                                student_second=student_second, student_third=student_third, 
                                session_first=session_first, session_second=session_second, 
                                session_third=session_third, title='Dashboard')
        else :
            return "this page is only for teacher", 403
    else:
        return "this page is only for teacher", 403  

@login_required
@app.route('/dashboard/<string:grade>', methods=['GET', 'POST'])
def dashboard_grade(grade):
    if current_user.is_authenticated:
        if current_user.email==('teacher@elsheko.com'):
                all_data = get_by_grade(grade)
                students = Student.query.filter_by(grade=grade).all() 
                session = Session.query.filter_by(grade=grade).all()
                return render_template('dashboard_grade.html', all_students=all_data, 
                                       students=students, sessions=session, 
                                       title='dashboard_grade')
        else:
            return "Unauthorized access", 403
    else:
        return "Unauthorized access", 403  

@login_required
@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    if current_user.is_authenticated :
        if current_user.id == id or current_user.email==('teacher@elsheko.com') :
            student = Student.query.filter_by(id=id).first()
            all_session = Session.query.filter_by(grade=student.grade).all()
            student_attended = sorted(student.attended, key=lambda session: session.id)
            student_marks = db.session.query(Student_Session).filter(Student_Session.c.student_id==id).order_by(Student_Session.c.session_id).all()
            if student:
                return render_template('student_profile.html', student=student,
                                    marks=student_marks, attended=student_attended,
                                      sessions=all_session, title='Profile')
        else :
            return "you can only view your profile", 403
    else:
        return "you can only view your profile", 403

@login_required
@app.route('/create_session/<string:grade>', methods=['GET', 'POST'])
def evaluate(grade):
    if current_user.is_authenticated:
        if current_user.email==('teacher@elsheko.com'):
            students = Student.query.filter_by(grade=grade).all()
            
            form = Submit_Student_mark()
            new_session = Session(grade=grade)
            if form.validate_on_submit():
                db.session.add(new_session)
                db.session.commit()
                for student, student_form in zip(students, form.students_list):
                    student_session_entry = Student_Session.insert().values(
                        student_id=student.id,
                        session_id=new_session.id,
                        mark=student_form.quiz_mark.data,
                        full_mark=form.quiz_full_mark.data
                    )
                    db.session.execute(student_session_entry)
                db.session.commit()
                return redirect(url_for('dashboard_grade', grade=grade))
            else:
                print("Form validation failed!")
                print(form.errors)
        return render_template('evalute.html', form=form, session=new_session, 
                               students=students, title='create_session')
    else:
        return "Unauthorized access", 403

@app.route('/session/<string:grade>', methods=['GET', 'POST'])
def create_session(grade):
    if current_user.is_authenticated:
        if current_user.email==('teacher@elsheko.com'):
            form = SessionForm()
            if form.validate_on_submit():
                session = Session(title=form.title.data, 
                                  description=form.description.data,
                                    attachment_link=form.attachment_link.data,
                                    video_link = form.video_link.data,
                                      grade=grade)
                db.session.add(session)
                db.session.commit()
                return redirect(url_for('dashboard_grade', grade=grade))
            else:
                print("Form validation failed!")
                print(form.errors)
            return render_template('session_info_form.html', form=form, title='session_info_form')
        else:
            return "Unauthorized access", 403
        
@app.route('/session/<int:id>', methods=['GET', 'POST'])
def session_info_for_student(id):
    if current_user.is_authenticated:
        session = Session.query.filter_by(id=id).first()
        return render_template('session_info.html', session=session, title='session_info')
    else:
        return "Unauthorized access", 403

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.photo_link)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

"""
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