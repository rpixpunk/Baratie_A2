from App.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name