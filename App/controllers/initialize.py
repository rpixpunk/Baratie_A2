from .user import create_course_admin
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_course_admin('bob', 'bobpass')
