from App.models import Course
from App.database import db

def create_course(name, description):
    course = Course(name=name, description=description)
    db.session.add(course)
    db.session.commit()
    print(name + " has been created")