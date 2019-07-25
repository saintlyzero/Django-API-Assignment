from ..models import Employees


class EmployeeService:
    

    def add_employee(data):
        print('inside Service')
        fname = data["firstname"]
        lname = data["lastname"]
        empid = data["emp_id"]
        emp = Employees(firstname=fname,lastname=lname,emp_id=empid)
        emp.save()
