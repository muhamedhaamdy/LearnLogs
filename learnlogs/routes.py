import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from learnlogs import app, db, bcrypt
from learnlogs.forms import EnrollForm, LoginForm, Submit_Student_mark, SessionForm
from learnlogs.models import Student, Session, Student_Session
from flask_login import login_user, current_user, logout_user, login_required
from learnlogs.data import get_by_grade, get_top, get_list_of_student_marks


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    """Home page

    Returns:
        HTML home page: home page
    """
    return render_template('home.html')


@app.route("/enroll", methods=['GET', 'POST'])
def enroll():
    """enroll page

    Returns:
        the enroll page: this page to register a new student
    """
    # if current_user.  uthenticated:
    #     return redirect(url_for('home'))
    form = EnrollForm()
    photo_file = 'default.jpg'
    if form.photo_link.data:
        photo_file = save_picture(form.photo_link.data)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        student = Student(
            student_name=form.student_name.data,
            email=form.email.data,
            password=hashed_password,
            student_phone=form.student_phone.data,
            parent_name=form.parent_name.data,
            parent_phone=form.parent_phone.data,
            address=form.address.data,
            photo_link=photo_file,
            grade=form.grade.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template('new-enroll.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """login page

    Returns:
        the login page: this page to login as a student or teacher
    """
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'teacher@elsheko.com' and form.password.data == '1234':
            login_user(
                Student.query.filter_by(
                    email='teacher@elsheko.com').first(),
                remember=False)
            return redirect(url_for('dashboard'))
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(
                student.password, form.password.data):
            login_user(student, remember=False)
            return redirect(url_for('profile1', id=student.id))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('index.html', title='Login', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """dashboard page

    Returns:
        the dashboard: the dashboard page for the teacher
    """
    if current_user.is_authenticated:
        if current_user.email == ('teacher@elsheko.com'):
            student_first = len(Student.query.filter_by(grade='first').all())
            student_second = len(Student.query.filter_by(grade='second').all())
            student_third = len(Student.query.filter_by(grade='third').all())
            session_first = len(Session.query.filter_by(grade='first').all())
            session_second = len(Session.query.filter_by(grade='second').all())
            session_third = len(Session.query.filter_by(grade='third').all())
            top_student_first = get_top('first')
            first_element = next(iter(top_student_first.items()))
            first_value1 = first_element[1]
            top_student_second = get_top('second')
            first_element = next(iter(top_student_second.items()))
            first_value2 = first_element[1]
            top_student_third = get_top('third')
            first_element = next(iter(top_student_third.items()))
            first_value3 = first_element[1]

            return render_template(
                'dashboard.html',
                student_first=student_first,
                student_second=student_second,
                student_third=student_third,
                session_first=session_first,
                session_second=session_second,
                session_third=session_third,
                top_student_first=first_value1,
                top_student_second=first_value2,
                top_student_third=first_value3,
                title='Dashboard')
        else:
           return render_template('error_page.html', title='Register', message='this page is only for teacher')
    else:
           return render_template('error_page.html', title='Register', message='this page is only for teacher')


@login_required
@app.route('/dashboard/<string:grade>', methods=['GET', 'POST'])
def dashboard_grade(grade):
    """dashboard_grade page

    Args:
        grade (string): input grade to show the dashboard for this grade

    Returns:
        the grade page: the dashboard page for the teacher for a specific grade
    """
    if current_user.is_authenticated:
        if current_user.email == ('teacher@elsheko.com'):
            all_data = get_by_grade(grade)
            students = Student.query.filter_by(grade=grade).all()
            session = Session.query.filter_by(grade=grade).all()
            return render_template(
                'dashboard_grade.html',
                all_students=all_data,
                students=students,
                sessions=session,
                title='dashboard_grade')
        else:
           return render_template('error_page.html', title='Register', message='this page is only for teacher')
    else:
        return render_template('error_page.html', title='Register', message='this page is only for teacher')

@login_required
@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile1(id):
    """profile1 page

    Args:
        id (integer): the id of student

    Returns:
        the profile page: this page show the profile for student
    """
    if current_user.is_authenticated:
        if current_user.id == id or current_user.email == (
                'teacher@elsheko.com'):
            student = Student.query.filter_by(id=id).first()
            all_session = Session.query.filter_by(grade=student.grade).all()
            student_attended = sorted(
                student.attended, key=lambda session: session.id)
            student_marks = db.session.query(Student_Session).filter(
                Student_Session.c.student_id == id).order_by(
                Student_Session.c.session_id).all()
            if student:
                return render_template(
                    'profile.html',
                    student=student,
                    marks=student_marks,
                    attended=student_attended,
                    sessions=all_session,
                    title='Profile')
        else:
           return render_template('error_page.html', title='Register', message='you can only view your profile')
    else:
       return render_template('error_page.html', title='Register', message='you can only view your profile')


@app.route('/statistics/<int:id>', methods=['GET', 'POST'])
def profile2(id):
    """sratestics page

    Args:
        id (integer): the id of student

    Returns:
        return the statistics page: return the statistics page for the student
    """
    if current_user.is_authenticated:
        if current_user.id == id or current_user.email == (
                'teacher@elsheko.com'):
            student = Student.query.filter_by(id=id).first()
            all_session = Session.query.filter_by(grade=student.grade).all()
            student_attended = sorted(
                student.attended, key=lambda session: session.id)
            student_marks = db.session.query(Student_Session).filter(
                Student_Session.c.student_id == id).order_by(
                Student_Session.c.session_id).all()
            all_grade_data = get_by_grade(student.grade)
            student_data = all_grade_data[student.id]
            list_of_student_marks = get_list_of_student_marks(student)
            if student:
                return render_template(
                    'profile_stats.html',
                    student=student,
                    marks=student_marks,
                    attended=student_attended,
                    number_of_attended=len(student_attended),
                    sessions=all_session,
                    sessions_number=len(all_session),
                    precentage=student_data['precentage'],
                    list_of_student_marks=list_of_student_marks,
                    title='Profile')
        else:
           return render_template('error_page.html', title='Register', message='you can only view your profile')
    else:
        return render_template('error_page.html', title='Register', message='you can only view your profile')


@login_required
@app.route('/logs/<int:id>', methods=['GET', 'POST'])
def profile(id):
    """logs page for student

    Args:
        id (integer): id for the student

    Returns:
        the logs page: the logs page for the sessions and marks for the student
    """
    if current_user.is_authenticated:
        if current_user.id == id or current_user.email == (
                'teacher@elsheko.com'):
            student = Student.query.filter_by(id=id).first()
            all_session = Session.query.filter_by(grade=student.grade).all()
            student_attended = sorted(
                student.attended, key=lambda session: session.id)
            student_marks = db.session.query(Student_Session).filter(
                Student_Session.c.student_id == id).order_by(
                Student_Session.c.session_id).all()
            if student:
                return render_template(
                    'profile_logs.html',
                    student=student,
                    marks=student_marks,
                    attended=student_attended,
                    sessions=all_session,
                    title='Profile')
        else:
           return render_template('error_page.html', title='Register', message='you can only view your profile')
    else:
       return render_template('error_page.html', title='Register', message='you can only view your profile')


@login_required
@app.route('/envaluate/<string:grade>', methods=['GET', 'POST'])
def envaluate_session(grade):
    """envaluate_session page

    Args:
        grade (string): grade of student

    Returns:
        envaluate page: to set the marks and attedence for the students
    """
    if current_user.is_authenticated:
        if current_user.email == ('teacher@elsheko.com'):
            all_sessions = Session.query.filter_by(grade=grade).all()
            all_data = db.session.query(Student_Session).all()
            all_session_created = []
            for info in all_data:
                all_session_created.append(info.session_id)
            return render_template(
                'evaluate_session.html',
                sessions=all_sessions,
                session_ids=all_session_created,
                title='envaluate')
        else:
           return render_template('error_page.html', title='Register', message='you can only view your profile')
    else:
       return render_template('error_page.html', title='Register', message='you can only view your profile')


@login_required
@app.route('/evaluate/<string:grade>/<int:id>', methods=['GET', 'POST'])
def evaluate(grade, id):
    """envaluate_session page

    Args:
        grade (string): grade of student

    Returns:
        envaluate page: to set the marks and attedence for the students
    """
    if current_user.is_authenticated:
        if current_user.email == ('teacher@elsheko.com'):
            students = Student.query.filter_by(grade=grade).all()
            form = Submit_Student_mark()
            if form.validate_on_submit():
                for student, student_form in zip(students, form.students_list):
                    student_session_entry = Student_Session.insert().values(
                        student_id=student.id,
                        session_id=id,
                        mark=student_form.quiz_mark.data,
                        full_mark=form.quiz_full_mark.data
                    )
                    db.session.execute(student_session_entry)
                db.session.commit()
                return redirect(url_for('dashboard_grade', grade=grade))
            else:
                print("Form validation failed!")
                print(form.errors)
        return render_template('evalute.html', form=form,
                               students=students, title='create_session')
    else:
       return render_template('error_page.html', title='Register', message='Unauthorized access')


@app.route('/session/<string:grade>', methods=['GET', 'POST'])
def create_session(grade):
    """Create new seesion page

    Args:
        grade (string): grade of student

    Returns:
        Session page: to create a new session for the teacher
    """
    if current_user.is_authenticated:
        if current_user.email == ('teacher@elsheko.com'):
            form = SessionForm()
            if form.validate_on_submit():
                attachment_file = 'default.pdf'
                video_file = 'default.mp4'
                if form.attachment_link.data:
                    attachment_file = save_path(
                        form.attachment_link.data, 'static/attachments')
                if form.video_link.data:
                    video_file = save_path(
                        form.video_link.data, 'static/images')
                session = Session(title=form.title.data,
                                  description=form.description.data,
                                  attachment_link=attachment_file,
                                  video_link=video_file,
                                  grade=grade)
                db.session.add(session)
                db.session.commit()
                return redirect(url_for('dashboard_grade', grade=grade))
            else:
                print("Form validation failed!")
                print(form.errors)
            return render_template(
                'session_info_form.html',
                form=form,
                title='session_info_form')
        else:
           return render_template('error_page.html', title='Register', message='Unauthorized access')


@app.route('/session/<int:id>', methods=['GET', 'POST'])
def session_info_for_student(id):
    if current_user.is_authenticated:
        session = Session.query.filter_by(id=id).first()
        return render_template(
            'session_info.html',
            session=session,
            title='session_info')
    else:
       return render_template('error_page.html', title='Register', message='Unauthorized access')


@login_required
@app.route('/all_session/<string:grade>', methods=['GET', 'POST'])
def all_session_grade(grade):

    if current_user.is_authenticated:
        if current_user.id == id or current_user.email == (
                'teacher@elsheko.com'):
            all_session = Session.query.filter_by(grade=grade).all()

            if all_session:
                return render_template(
                    'all_session_grade.html',sessions=all_session,student =current_user,
                    title='session_grade')
        else:
           return render_template('error_page.html', title='Register', message='you can only view your profile')
    else:
       return render_template('error_page.html', title='Register', message='you can only view your profile')




@login_required
@app.route("/logout")
def logout():
    """Logout

    Returns:
        logout page: to logout from the system
    """
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    """Sava a Photo

    Args:
        form_picture (straing): name of the photo

    Returns:
        hashing string: the new name of the photo
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_path(form_attachment, path):
    """Sava a file or video

    Args:
        form_picture (straing): name of the file or video

    Returns:
        hashing string: the new name of the file or video
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_attachment.filename)
    attachment_fn = random_hex + f_ext
    attachment_path = os.path.join(app.root_path, path, attachment_fn)

    # output_size = (125, 125)
    # i = Image.open(form_attachment)
    # i.thumbnail(output_size)
    form_attachment.save(attachment_path)
    return attachment_fn


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
