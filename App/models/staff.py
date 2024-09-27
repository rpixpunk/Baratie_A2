<<<<<<< HEAD
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(120), nullable=False)

    def __init__(self, name, role):
        self.name = name
        self.role = role
=======

>>>>>>> 715743bdaecf43ac01d13ee2776ddbde426e4e37
