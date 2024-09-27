from App.database import db

class CourseStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('course_staff', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('course_staff', lazy=True))

    def __init__(self, courseID, staffID):
        self.courseID = courseID
        self.staffID = staffID