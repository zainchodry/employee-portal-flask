from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()



class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)
    location = db.Column(db.String(100), nullable = True)

    def __repr__(self) -> str:
        return f"{self.name} - {self.location}"
    


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)

    def __repr__(self) -> str:
        return self.name
    



class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    bonus = db.Column(db.Integer, nullable=True)
    
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    role = db.relationship("Role", backref="employees")

    Dept_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    department = db.relationship("Department", backref="employees")

    phone = db.Column(db.String(20), nullable=False)
    hire_date = db.Column(db.Date, default=datetime.today, nullable=False)

    def __repr__(self) -> str:
        return f"{self.firstname} - {self.lastname} - {self.phone}"



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = False)


    def __repr__(self) -> str:
        return f"{self.username} - {self.email}"
    
    