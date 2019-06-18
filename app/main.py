from flask import Flask, request
from flask_restful import Api, Resource

from app.db_models import Employee, Department


app = Flask(__name__)
api = Api(app)


def is_json(f):
    def new_func(*args, **kwargs):
        if request.is_json:
            return f(*args, **kwargs)
        else:
            return {}, 415
    return new_func
        
        
class DepartmentApi(Resource):
    def get(self):
        departments = Department.select(Department.name_department)
        return {'data': [dep.name_department
                            for dep in departments]}, 200
    @is_json
    def post(self):
        try:
            department = Department.create(**request.json)
        except IntegrityError:
            return {}, 409
        else:
            department.save()
            return {'data': request.json}
        
    @is_json
    def delete(self):
        name = request.json.get('name')
        if name is None:
            return {}, 400
        department = Department.delete().where(
            Department.name_department == name
        )
        department.execute()
        return {}, 200


 
api.add_resource(DepartmentApi, '/department')


if __name__ == '__main__':
    connect(database='postgres', user='postgres')
    app.run(debug=True)
