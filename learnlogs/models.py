from datetime import datetime
from learnlogs import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_student(user_id):
    return Student.query.get(int(user_id))

Student_Session = db.Table('student_session', 
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                           db.Column('session_id', db.Integer, db.ForeignKey('session.id')),
                           db.Column('mark', db.Integer, default=None),
                           db.Column('full_mark', db.Integer, default=10))

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    student_phone = db.Column(db.String(11), nullable=False)
    parent_name = db.Column(db.String(60), nullable=False)
    parent_phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    photo_link = db.Column(db.String(100), default='default.jpg')
    grade = db.Column(db.String(10), nullable=False)    
    attended = db.relationship('Session', secondary=Student_Session, backref='attended_student')

    def __repr__(self):
        return f"Enroll('{self.student_name}', '{self.email}', '{self.grade}')"

class Session(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    attachment_link = db.Column(db.String(100), default='default.pdf')
    video_link = db.Column(db.String(100), default='default.mp4')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    grade = db.Column(db.String(10), nullable=False)
    students = db.relationship('Student', secondary=Student_Session, backref='sessions')

    def __repr__(self):
        return f"Session('{self.id}', '{self.date}', '{self.grade}')"
