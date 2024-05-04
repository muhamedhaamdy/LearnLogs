from learnlogs import app, db
from sqlalchemy import select
from learnlogs.models import Session, Student, Student_Session
from learnlogs.data import get_by_grade, get_top,get_list_of_student_marks

with app.app_context():
    db.drop_all()
    db.create_all()

    saad = Student(student_name='saad', email='saad@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='saad parent', parent_phone='12345678901', address='saad address', grade='first')
    umar = Student(student_name='umar', email='umar@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='umar parent', parent_phone='12345678901', address='umar address', grade='second')
    bor3y = Student(student_name='bor3y', email='bor3y@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='bor3y parent', parent_phone='12345678901', address='bor3y address', grade='first')
    hazems = Student(student_name='hazems', email='hazme@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='hazems parent', parent_phone='12345678901', address='hazems address', grade='third')
    khalil = Student(student_name='khalil', email='khalil@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='khalil parent', parent_phone='12345678901', address='khalil address', grade='first')
    abdo = Student(student_name='abdo', email='abdo@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='abdo parent', parent_phone='12345678901', address='abdo address', grade='second')
    swefy = Student(student_name='swefy', email='swefy@mirna.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='swefy parent', parent_phone='12345678901', address='swefy address', grade='first')
    hoda = Student(student_name='hoda', email='hoda@elsheko.com', password='pas$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBOsword', student_phone='12345678901', parent_name='swefy parent', parent_phone='12345678901', address='hoda address', grade='third')
    youssef = Student(student_name='youssef', email='yousssef@elwakil.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='salah', parent_phone='12345678901', address='youssef address', grade='second')
    teacher = Student(student_name='teacher', email='teacher@elsheko.com', password='$2b$12$4HKAnkwr1uqmtbLsZsNHleYLAspcYhmx3ZEAr8AequRzFnY21MUBO', student_phone='12345678901', parent_name='teacher parent', parent_phone='12345678901', address='teacher address', grade='teacher')

    db.session.add_all([saad, umar, bor3y, hazems, khalil, abdo, swefy, hoda, youssef, teacher])
    db.session.commit()

    # session_first1 = Session(title='Newton first law', description='bla bla', grade='first')
    # session_first2 = Session(title='Newton second law', description='bla bla', grade='first')
    # session_first3 = Session(title='Newton third law', description='bla bla', grade='first')
    # session_second1 = Session(title='Pythagoras law', description='bla bla', grade='second')
    # session_second2 = Session(title='Euclid law', description='bla bla', grade='second')
    # session_third1 = Session(title='quntam mechanics', description='bla bla', grade='third')
    # session_third2 = Session(title='quntam dynamics', description='bla bla', grade='third')

    # db.session.add_all([saad, umar, bor3y, hazems, khalil, abdo, swefy, hoda, youssef, teacher,
    #                      session_first1, session_first2, session_first3,
    #                        session_second1, session_second2, session_third1, session_third2])
    # db.session.commit()

    # student_session_entry1 = Student_Session.insert().values(student_id=saad.id, session_id=session_first1.id, mark=7)
    # student_session_entry2 = Student_Session.insert().values(student_id=saad.id, session_id=session_first2.id, mark=8)
    # student_session_entry3 = Student_Session.insert().values(student_id=saad.id, session_id=session_first3.id, mark=9)
    # student_session_entry4 = Student_Session.insert().values(student_id=swefy.id, session_id=session_first1.id, mark=3)
    # student_session_entry5 = Student_Session.insert().values(student_id=swefy.id, session_id=session_first2.id, mark=8)
    # student_session_entry6 = Student_Session.insert().values(student_id=swefy.id, session_id=session_first3.id, mark=10)
    # student_session_entry7 = Student_Session.insert().values(student_id=abdo.id, session_id=session_second1.id, mark=10)
    # student_session_entry8 = Student_Session.insert().values(student_id=abdo.id, session_id=session_second2.id, mark=10)
    # student_session_entry9 = Student_Session.insert().values(student_id=bor3y.id, session_id=session_first1.id, mark=5)
    # student_session_entry10 = Student_Session.insert().values(student_id=hazems.id, session_id=session_third2.id, mark=6)

    # db.session.execute(student_session_entry1)
    # db.session.execute(student_session_entry2)
    # db.session.execute(student_session_entry3)
    # db.session.execute(student_session_entry4)
    # db.session.execute(student_session_entry5)
    # db.session.execute(student_session_entry6)
    # db.session.execute(student_session_entry7)
    # db.session.execute(student_session_entry8)
    # db.session.execute(student_session_entry9)
    # db.session.execute(student_session_entry10)

    # db.session.commit()

    # top = get_top('first')
    # first_element = next(iter(top.items()))
    # first_value = first_element[1] 
    # print(first_value['precentage'])

    # mark1 = get_list_of_student_marks(saad)
    # print(mark1)
    # mark2 = get_list_of_student_marks(umar)
    # print(mark2)
    # mark3 = get_list_of_student_marks(bor3y)
    # print(mark3)


'''
    all_students_first = Student.query.filter_by(grade='first').all()
    all_students_second = Student.query.filter_by(grade='second').all()
    all_students_third = Student.query.filter_by(grade='third').all()

    all_session_first = Session.query.filter_by(grade='second').all()

    for student in all_students_first:
        student_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == student.id).all()
        total_mark_for_student = 0
        for mark in student_mark:
            total_mark_for_student += mark.mark
        print('student name: {} and his presentage is: {:.2f}%'.format(student.student_name ,
                                                                 100 * (total_mark_for_student / (len(all_session_first)*10))))
    all_session = Session.query.filter_by(grade=saad.grade).all()
    student_attended = sorted(saad.attended, key=lambda session: session.id)
    print(saad_mark)
'''