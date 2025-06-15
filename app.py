from flask import Flask,render_template, request, redirect, url_for, flash
from models import db, Department, Role, Employee, User
from datetime import date, datetime
from flask_migrate import Migrate
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)
with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/home', methods = ['GET'])
def home():
    return render_template("index.html")


@app.route('/view-employee/', methods = ['GET'])
def view_employee():
    employees = Employee.query.all()
    return render_template("view.html", employees = employees)


@app.route('/add-employee/', methods = ['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        role = request.form['role']
        dept = request.form['department']

        emp = Employee(
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            email = request.form['email'],
            salary = int(request.form['salary']),
            bonus = int(request.form['bonus']),
            role_id = role,
            Dept_id = dept,
            phone = int(request.form['phone']),
            hire_date = datetime.now()
        )
        db.session.add(emp)
        db.session.commit()
        return redirect(url_for('home'))


    return render_template("add.html")



@app.route('/delete-employee/<int:id>', methods = ['GET'])
def delete_employee(id):
    try:
        employees = Employee.query.get(id)
        if employees:
            db.session.delete(employees)
            db.session.commit()
            return redirect(url_for('home'))
    except Exception as e:
        print("Employee is Not Found", e)
        return redirect('/')
    

@app.route('/delete-employee/')
def delete():
    employees = Employee.query.all()
    return render_template("delete.html", employees=employees)


@app.route('/filter-employee/', methods=['GET', 'POST'])
def filter_employee():
    if request.method == 'POST':
        name = request.form['name'].strip()
        dept = request.form['department'].strip()
        role = request.form['role'].strip()

        employees = Employee.query

        if name:
            employees = employees.filter(
                or_(
                    Employee.firstname.ilike(f"%{name}%"),
                    Employee.lastname.ilike(f"%{name}%")
                )
            )
        if dept:
            employees = employees.join(Department).filter(Department.name.ilike(f"%{dept}%"))
        if role:
            employees = employees.join(Role).filter(Role.name.ilike(f"%{role}%"))

        employees = employees.options(joinedload(Employee.department), joinedload(Employee.role)).all()

        return render_template("view.html", employees=employees)

    return render_template("filter.html")



@app.route('/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Password do not Match", "danger")
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email = email).first():
            flash("Email Already Registered", "danger")
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account Created Successfully! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template("signup.html")



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in Successfully", "success")
            return redirect(url_for('home'))
        
        else:
            flash("Invalid Credentials", "danger")

    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug = True)