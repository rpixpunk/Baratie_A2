from App.models import Staff
from App.database import db

def create_staff(name, role):
    staff = Staff(name=name, role=role)
    try:
        db.session.add(staff)
        db.session.commit()
    except IntegrityError as e:
        print("Staff member already exists")
        db.session.rollback()
    else:
        print(name + " has been created and assigned to " + role)