from App.models import Course
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_course(name, description):
    course = Course(name=name, description=description)
    try:
        db.session.add(course)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("Course already exists")
    else:
        print(name + " has been created")