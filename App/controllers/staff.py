from App.models import Staff
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_staff(name, role):
    staff = Staff(name=name, role=role)
    try:
        db.session.add(staff)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("Staff member already exists")
    else:
        print(name + " has been created and assigned to " + role)