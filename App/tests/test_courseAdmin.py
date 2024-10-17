import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import CourseAdmin
from App.controllers import (
    create_course_admin,
    get_all_users_json,
    course_admin_login,
    create_staff,
    create_course,
    assign_staff,
    view_course_staff,
)

LOGGER = logging.getLogger(__name__)

'''
    Unit Tests
'''

class CourseAdminUnitTests(unittest.TestCase):
    
    def test_create_staff(self):
        staff_member = create_staff("John", "TA")
        assert staff_member.name == "John"
    
    def test_create_staff_fail(self):
        with pytest.raises(ValueError):
            create_staff("Jack", '')
    
    def test_create_course(self):
        course = create_course("Math", "Introductory Course")
        assert course.name == "Math"
    
    def test_create_course_fail(self):
        with pytest.raises(ValueError):
            create_course('', "Introductory Course")

    #def test_assign_staff(self):


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

'''
    Integration Tests
'''
