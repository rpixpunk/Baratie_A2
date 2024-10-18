from App.models import CourseStaff, Course, Staff
from App.database import db

def assign_staff(course_name, staff_name):
    course = Course.query.filter_by(name=course_name).first()
    staff = Staff.query.filter_by(name=staff_name).first()

    if not course or not staff:
        print("Cannot make assignment")
        raise TypeError
        return

    assigned = CourseStaff.query.filter_by(courseID=course.id, staffID=staff.id).first()
    if assigned:
       print("Staff member " + staff_name + " is already assigned to " + course_name) 
       return

    course_staff = CourseStaff(courseID=course.id, staffID=staff.id)
    db.session.add(course_staff)
    db.session.commit()
    print("Staff member " + staff_name + " has been assigned to " + course_name)
    return course_staff

def view_course_staff(course_name):
    course = Course.query.filter_by(name=course_name).first()
    
    if not course:
        print('Course not found.')
        return
    
    staff = course.course_staff
    if not staff:
        print('No staff members are assigned to this course.')
        return
    
    staff_members = [staff_member.staff.get_json() for staff_member in staff]
    print(staff_members)
    return staff_members