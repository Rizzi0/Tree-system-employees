from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta


fake = Faker()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Junior_tests'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')




# Создание фейковых данных для БД. 
def create_employee(name, position, hire_date, salary, manager=None):
    employee = Employee(name=name, position=position, hire_date=hire_date, salary=salary, manager=manager)
    db.session.add(employee)
    db.session.commit()



# Страница создания фейковых данных бля БД
@app.route("/", methods=["GET", "POST"])
def display_tree():
    if request.method == "POST":
        num = int(request.form.get("data"))
        for _ in range(num):
            if Employee.query.filter_by(id=1).first() is None:
                create_employee('Mars Mars', 'Seo', '2001-01-01', 30000)

            name = fake.name()
            position = fake.job()
            hire_date = (datetime.now() - timedelta(days=randint(1, 3650))).strftime('%Y-%m-%d')
            salary = round(randint(30000, 150000), 2)
            manager = choice(Employee.query.all())
            create_employee(name, position, hire_date, salary, manager=manager)


        db.session.commit()
        
    return render_template('index.html')



# Страница с древовидной структурой сотрудников
@app.route("/get", methods=["GET", "POST"])
def hierarchy():
    root_employee = Employee.query.filter_by(manager_id=None).first()
    return render_template('tree.html', root_employee=root_employee)



# Общий список сотрудников с возможность сортировки по разным параметрам
@app.route("/employees", methods=["GET", "POST"])
def employees():
    sort_field = request.args.get('sort_field', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    if sort_order == 'asc':
        sort_order_func = asc
    else:
        sort_order_func = desc
    
    employees = Employee.query.order_by(sort_order_func(sort_field)).all()
    return render_template('employees.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True)
