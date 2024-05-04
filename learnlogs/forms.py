from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_wtf.form import _Auto
from learnlogs.models import Student
from wtforms import FormField, FieldList, StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange


class EnrollForm(FlaskForm):
    """Enroll Form"""
    student_name = StringField('Student Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Enter a password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password"})
    student_phone = StringField('Student Phone', validators=[DataRequired()], render_kw={"placeholder": "Enter your phone number"})
    parent_name = StringField('Parent Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your parent's name"})
    parent_phone = StringField('Parent Phone', validators=[DataRequired()], render_kw={"placeholder": "Enter your parent's phone number"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Enter your address"})
    photo_link = StringField('Photo Link', render_kw={"placeholder": "Enter the URL of your photo (optional)"})
    grade = StringField('Grade', validators=[DataRequired()], render_kw={"placeholder": "Enter your grade"})
    enroll = SubmitField('Enroll')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email',
                    validators=[DataRequired(), Email()],
                    render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your Password"})
    submit = SubmitField('Login')


class QuizForm(FlaskForm):
    """Quiz Form"""
    absent = BooleanField('Absent')
    quiz_mark = IntegerField('Quiz Mark')


class Submit_Student_mark(FlaskForm):
    """Submit Student Mark Form"""
    quiz_full_mark = IntegerField(
        'Quiz Full Mark', validators=[
            InputRequired(), NumberRange(
                min=0, max=100)])
    students_list = FieldList(FormField(QuizForm), min_entries=1000)
    submit = SubmitField('Submit')


class SessionForm(FlaskForm):
    """Session Form"""
    title = StringField('Session Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    attachment_link = FileField('Attachment Link', validators=[
                                FileAllowed(['pdf', 'docx', 'pptx'])])
    video_link = FileField('Video Link', validators=[
                           FileAllowed(['mp4', 'mov', 'avi'])])
    submit = SubmitField('Submit')

    # def validate_quiz_mark(self, quiz_mark):
    #     if self.absent.data == False and self.quiz_mark.data > self.quiz_full_mark.data:
    #         raise ValidationError('Quiz mark should be less than or equal to the full mark')
    #     if self.absent.data == True and self.quiz_mark.data != 0:
    #         raise ValidationError('Quiz mark should be zero if student is absent')
