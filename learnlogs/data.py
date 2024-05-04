from learnlogs.models import Student, Session, Student_Session
from learnlogs import db

all_student_data = {}


def get_by_grade(grade):
    all_students = Student.query.filter_by(grade=grade).all()
    all_session = Session.query.filter_by(grade=grade).all()
    for student in all_students:
        student_mark = db.session.query(Student_Session).filter(
            Student_Session.c.student_id == student.id).all()
        all_mark = []
        total_mark_for_student = 0
        for mark in student_mark:
            all_mark.append({'session': mark.session_id,
                            'mark': mark.mark, 'full_mark': mark.full_mark})
            if mark.mark is not None and mark.full_mark is not None:
                total_mark_for_student += mark.mark / mark.full_mark
            else:
                continue
        if len(all_session) == 0:
            total_mark_precision = 0
        else:
            total_mark_precision = total_mark_for_student / len(all_session) * 100
        all_student_data[student.id] = {'student_name': student.student_name,
                                        'email': student.email,
                                        'grade': student.grade,
                                        'student_phone': student.student_phone,
                                        'parent_phone': student.parent_phone,
                                        'address': student.address,
                                        'mark': all_mark,
                                        'attendance': student.attended,
                                        'precentage': total_mark_precision}
    return all_student_data


def get_top(grade):
    all_student_data = {}
    all_students = Student.query.filter_by(grade=grade).all()
    all_data = get_by_grade(grade)
    for student in all_students:
        all_student_data[student.id] = {
            'student_name': student.student_name, 'precentage': all_data[student.id]['precentage']}
    all_student_data = dict(
        sorted(
            all_student_data.items(),
            key=lambda item: item[1]['precentage'],
            reverse=True))
    return all_student_data


def get_list_of_student_marks(student):
    all_grade_data = get_by_grade(student.grade)
    student_data = all_grade_data[student.id]
    all_session_in_same_grade = Session.query.filter_by(
        grade=student.grade).all()

    all_session_in_same_grade_by_id = []
    for session in all_session_in_same_grade:
        all_session_in_same_grade_by_id.append(session.id)

    student_mark = []
    for mark in student_data['mark']:
        if mark['session'] in all_session_in_same_grade_by_id:
            student_mark.append(mark['mark'] / mark['full_mark'])
        else:
            student_mark.append(0)

    # Make the length of student_mark equal to 10
    student_mark.extend([0] * (10 - len(student_mark)))

    return student_mark
