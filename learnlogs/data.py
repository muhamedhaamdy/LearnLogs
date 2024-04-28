from learnlogs.models import Student, Session, Student_Session
from learnlogs import db

all_student_data = {}

def get_by_grade(grade):
    all_students = Student.query.filter_by(grade=grade).all()
    all_session = Session.query.filter_by(grade=grade).all()
    for student in all_students:
        student_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == student.id).all()
        all_mark = []
        total_mark_for_student = 0
        for mark in student_mark:
            all_mark.append({'session':mark.session_id, 'mark':mark.mark, 'full_mark':mark.full_mark})
            if mark.mark is not None and mark.full_mark is not None:
                total_mark_for_student += mark.mark / mark.full_mark
            else:
                continue
        total_mark_precision = total_mark_for_student/len(all_session) * 100        
        all_student_data[student.id]=[{'student_name':student.student_name, 'email':student.email, 
                                       'grade':student.grade, 'student_phone':student.student_phone,
                                         'parent_phone': student.parent_phone, 'address':student.address,
                                           'mark':all_mark,'attendance':student.attended,
                                             'precentage':total_mark_precision}]
    return all_student_data