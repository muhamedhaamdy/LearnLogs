from learnlogs import app, db
from sqlalchemy import select
from learnlogs.models import Session, Student, Student_Session


with app.app_context():
    db.drop_all()
    db.create_all()

'''
    saad = Student(student_name='saad', email='saad@elsheko.com', password='password', student_phone='12345678901', parent_name='saad parent', parent_phone='12345678901', address='saad address', grade='first')
    umar = Student(student_name='umar', email='umar@elsheko.com', password='password', student_phone='12345678901', parent_name='umar parent', parent_phone='12345678901', address='umar address', grade='first')
    bor3y = Student(student_name='bor3y', email='bor3y@elsheko.com', password='password', student_phone='12345678901', parent_name='bor3y parent', parent_phone='12345678901', address='bor3y address', grade='first')
    hazems = Student(student_name='hazems', email='hazme@elsheko.com', password='password', student_phone='12345678901', parent_name='hazems parent', parent_phone='12345678901', address='hazems address', grade='first')
    
    session1 = Session(grade='first')
    session2 = Session(grade='first')
    session3 = Session(grade='first')


    db.session.add_all([saad, umar, bor3y, hazems, session1, session2, session3])
    db.session.commit()

    student_session_entry1 = Student_Session.insert().values(student_id=saad.id, session_id=session1.id, mark=7)
    student_session_entry2 = Student_Session.insert().values(student_id=saad.id, session_id=session2.id, mark=8)
    student_session_entry3 = Student_Session.insert().values(student_id=saad.id, session_id=session3.id, mark=9)
    student_session_entry4 = Student_Session.insert().values(student_id=hazems.id, session_id=session2.id, mark=0)
    hazems.attended.append(session1)
    hazems.attended.append(session3)
    db.session.execute(student_session_entry1)
    db.session.execute(student_session_entry2)
    db.session.execute(student_session_entry3)
    db.session.execute(student_session_entry4)
    db.session.commit()

    saad_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == saad.id).all()
    all_session = Session.query.filter_by(grade=saad.grade).all()
    student_attended = sorted(saad.attended, key=lambda session: session.id)


    print(saad_mark)
'''