from App.models import CourseAdmin
from App.database import db

def create_course_admin(username, password):

    newuser = CourseAdmin(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None