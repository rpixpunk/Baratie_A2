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

    def test_assign_staff(self):
        staff_member = create_staff("James", "TA")
        course = create_course("Spanish", "Introductory Course")
        print(course.name)
        print(staff_member.name)
        assignment = assign_staff(course.name, staff_member.name)
        assert assignment.staffID == staff_member.id
        assert assignment.courseID == course.id

    def test_assign_staff_fail(self):
        # Create a course and a staff member
        staff_member = create_staff("Jeff", "TA")
        course = create_course("French", "Introductory Course")
        
        # Try assigning with invalid staff ID 
        with pytest.raises(TypeError):
            assign_staff(999, course.id) 
        
        # Try assigning with invalid course ID 
        with pytest.raises(TypeError):
            assign_staff(staff_member.id, 999) 

        # Try assigning with both invalid staff and course ID
        with pytest.raises(TypeError):
            assign_staff(999, 999)  


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

'''
    Integration Tests
'''

class CourseAdminIntegrationTests(unittest.TestCase):
    def test_create_and_assign_staff_to_course(self):


        client = self.app.test_client()
        response = client.post('/create-staff', json={'name': 'John', 'role': 'TA'})
        assert response.status_code == 200
        staff_id = response.json['id']
        
        response = client.post('/create-course', json={'name': 'Math', 'description': 'Introductory Course'})
        assert response.status_code == 200
        course_id = response.json['id']
        

        response = client.post(f'/assign-staff', json={'staff_id': staff_id, 'course_id': course_id})
        assert response.status_code == 200
        assert response.json['staff_id'] == staff_id
        assert response.json['course_id'] == course_id
        

        response = client.get(f'/course/{course_id}/staff')
        assert response.status_code == 200
        assert len(response.json['staff']) > 0
        assert response.json['staff'][0]['id'] == staff_id