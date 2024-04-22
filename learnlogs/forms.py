from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from learnlogs.models import Student
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange


class EnrollForm(FlaskForm):
    student_name = StringField('Student Name',
                           validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    student_phone = StringField('Student Number',   
                           validators=[DataRequired(), Length(min=11, max=11)])
    parent_name = StringField('Parent Name',
                           validators=[DataRequired()])
    parent_phone = StringField('Parent Number',
                           validators=[DataRequired(), Length(min=11, max=11)])
    address = StringField('Address',
                           validators=[DataRequired()])
    photo_link = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    grade = SelectField('Grade', choices=[('first', 'first'), 
                                          ('second', 'second'), ('third', 'third')], validators=[InputRequired()])

    enroll = SubmitField('enroll')
    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuizForm(FlaskForm):
    absent = BooleanField('Absent')
    quiz_mark = IntegerField('Quiz Mark', validators=[InputRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')

class SubmibButton(FlaskForm):
    quiz_full_mark = IntegerField('Quiz Full Mark', validators=[InputRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')
    # def validate_quiz_mark(self, quiz_mark):
    #     if self.absent.data == False and self.quiz_mark.data > self.quiz_full_mark.data:
    #         raise ValidationError('Quiz mark should be less than or equal to the full mark')
    #     if self.absent.data == True and self.quiz_mark.data != 0:
    #         raise ValidationError('Quiz mark should be zero if student is absent')