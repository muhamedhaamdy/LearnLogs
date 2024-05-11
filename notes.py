# This file is used to test the models and the relationships between them
'''
from learnlogs import app, db
from learnlogs.models import Session, Student, Student_Session

with app.app_context():
    db.create_all()

    #to get saad and umar(students) from the database
    saad = Student.query.filter_by(student_name='saad').first()
    umar = Student.query.filter_by(student_name='umar').first()
    
    #to get the session from the database
    session = Session.query.filter_by(id=1).first()

    #make saad and umar attend the session
    saad.attended.append(session)
    umar.attended.append(session)

    db.session.commit()

    #to get the students who attended the session
    attended = session.attended_student --> #attended_student is the backref in the Session model
    print(attended)

    #to get the sessions attended by saad
    saad_session = saad.attended --> #attended is the attribute in the Student model
    print(saad_session)
'''


#to test the many to many relationship between the Student and the Session models
'''

from learnlogs import app, db
from sqlalchemy import select
from learnlogs.models import Session, Student, Student_Session


with app.app_context():
    db.drop_all()
    db.create_all()

    
    #creating the students and the sessions
    saad = Student(student_name='saad', email='saad@gmail.com', password='password', student_phone='12345678901', parent_name='saad parent', parent_phone='12345678901', address='saad address', grade='first')
    umar = Student(student_name='umar', email='umar@gmail.com', password='password', student_phone='12345678901', parent_name='umar parent', parent_phone='12345678901', address='umar address', grade='first')
    bor3y = Student(student_name='bor3y', email='bor3y@gmail.com', password='password', student_phone='12345678901', parent_name='bor3y parent', parent_phone='12345678901', address='bor3y address', grade='first')
    session1 = Session(grade='first')
    session2 = Session(grade='first')
    session3 = Session(grade='first')


    db.session.add_all([saad, umar, bor3y, session1, session2, session3])
    db.session.commit()

    
    #creating the student_session entries for the students and the sessions
    #mark is the mark the student got in the session
    student_session_entry1 = Student_Session.insert().values(student_id=saad.id, session_id=session1.id, mark=7)
    student_session_entry2 = Student_Session.insert().values(student_id=umar.id, session_id=session1.id, mark=8)
    student_session_entry3 = Student_Session.insert().values(student_id=bor3y.id, session_id=session1.id, mark=9)
    db.session.execute(student_session_entry1)
    db.session.execute(student_session_entry2)
    db.session.execute(student_session_entry3)
    db.session.commit()

    #to get the mark of the students in the session
    saad_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == saad.id).first().mark
    umar_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == umar.id).first().mark
    bor3y_mark = db.session.query(Student_Session).filter(Student_Session.c.student_id == bor3y.id).first().mark
    
    print(saad_mark)
    print(umar_mark)
    print(bor3y_mark)
    



'''



'''
    لو انت عايزه يحضر عافيه من غير درجه هنعمل 
    saad.attended.append(session1)
    لو عايزه يحضر بدرجه حتي لو صفر هنعمل كده
    student_session_entry1 = Student_Session.insert().values(student_id=saad.id, session_id=session1.id, mark=7)
    وتكتب الدرحه اللي عايزها في القيمه اللي هتتحط في الجدول
'''
#https://github.com/StartBootstrap/startbootstrap-landing-page
#https://github.com/zuramai/mazer?tab=readme-ov-file
#https://github.com/mdbootstrap/bootstrap-5-admin-template/