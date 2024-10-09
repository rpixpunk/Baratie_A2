from App.models import Staff
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_staff(name, role):
    staff_member = Staff.query.filter_by(name=name, role=role).first()
    if staff_member:
       print("Staff member " + name + " is already assigned to " + role) 
       return
    
    staff = Staff(name=name, role=role)
    try:
        db.session.add(staff)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("Staff member already exists")
    else:
        print(name + " has been created and assigned to " + role)
        return staff