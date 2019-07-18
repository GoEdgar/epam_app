import peewee

from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource

from db_models import Employee, Department

app = Flask(__name__)
api = Api(app)


def is_json(f):
    def new_func(*args, **kwargs):
        if request.is_json:
            return f(*args, **kwargs)
        else:
            return {}, 415

    return new_func


def obj_to_dict(obj):
    return {field: getattr(obj, field) for field in obj._meta.fields}


class DepartmentsApi(Resource):
    def get(self):
        departments = Department.select()

        return {'data': [obj_to_dict(dep)
                         for dep in departments]
                }, 200

    @is_json
    def post(self):
        try:
            department = Department.create(**request.json)

        except peewee.DataError:
            return {'error': 'Invalid data type'}, 415

        except peewee.IntegrityError:
            return {'error': "It's a duplicate"}, 409

        else:
            dep_dict = request.json
            dep_dict['id'] = department.id
            department.save()
            return {'data': dep_dict}


class DepartmentApi(Resource):
    def get(self, dep_id):
        dep = Department.select().where(Department.id == dep_id)
        try:
            dep = dep[0]
        except IndexError:
            return {'error': 'Department not found'}, 404
        else:

            return {'data': {'id': dep.id,
                             'name_department': dep.name_department
                             }
                    }, 200

    def delete(self, dep_id):
        Department.delete_by_id(dep_id)
        return {}, 200


def emp_to_dict(emp):
    emp_dict = {'id': emp.id,
                'name_department': emp.name_department.name_department,
                'full_name': emp.full_name,
                'date_of_brith': emp.date_of_brith.isoformat(),
                'salary': emp.salary
                }
    return emp_dict


class EmployeesApi(Resource):
    def get(self):
        employees = Employee.select().join(Department)

        data = {'data': [emp_to_dict(emp) for emp in employees]}

        if not len(data['data']):
            return {'error': 'No employees'}, 404

        return data, 200

    @is_json
    def post(self):

        emp_dict = {field: request.json.get(field) for field in ['full_name',
                                                                 'name_department',
                                                                 'date_of_brith',
                                                                 'salary']}

        if None in emp_dict.values():
            return {'error': 'One of the parameters is missing or it is not'}, 400

        try:
            employee = Employee.create(**emp_dict)

        except peewee.DataError:
            return {'error': 'Invalid data type'}, 415

        except peewee.IntegrityError:
            return {}, 409
        except:
            return {}, 500
        else:
            emp_dict['id'] = employee.id
            employee.save()
            return {'data': emp_dict}, 200


class EmployeeApi(Resource):
    def get(self, emp_id):
        emp = Employee.select().where(Employee.id == emp_id)
        try:
            emp = emp[0]
        except IndexError:
            'Employee not found'
        else:
            return {'data': emp_to_dict(emp)}, 200

    @is_json
    def put(self, emp_id):
        emp_dict = {field: request.json.get(field) for field in ['full_name',
                                                                 'name_department',
                                                                 'date_of_brith',
                                                                 'salary']}
        if emp_dict['date_of_brith'] is not None:
            return {'error': 'Date of birth cannot be changed'}, 400

        emp_dict_keys = list(emp_dict.keys())
        for k in emp_dict_keys:
            if emp_dict[k] is None:
                emp_dict.pop(k)

        count_of_updates = Employee.update(emp_dict).where(
            Employee.id == emp_id).execute()

        if count_of_updates == 0:
            return {'error': 'Employee not found'}, 404

        emp = Employee.select().where(Employee.id == emp_id)[0]

        return {'data': emp_to_dict(emp)}, 200

    def delete(self, emp_id):
        Employee.delete_by_id(emp_id)
        return {}, 200


api.add_resource(DepartmentsApi, '/department/')
api.add_resource(DepartmentApi, '/department/<int:dep_id>')
api.add_resource(EmployeesApi, '/employee/')
api.add_resource(EmployeeApi, '/employee/<int:emp_id>')

if __name__ == '__main__':
    # connect(database='postgres', user='postgres')
    app.run()
