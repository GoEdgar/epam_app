from flask import Flask, request
from flask_restful import Api, Resource, marshal_with

from app.db_models import *

app = Flask(__name__)
api = Api(app)




class DepartmentApi(Resource):
    def get(self):
        departments = Department.select(Department.name_department)
        return {'data':[dep.name_department for dep in departments]}, 200
    
    def post(self):
        if request.content_type == 'application/json':
            try:
                department = Department.create(**request.json)
            except IntegrityError:
                return {}, 409
            else:
                department.save()
                return {'data': request.json}

    def delete(self):
        if request.content_type == 'application/json':
            try:
                department = Department.delete().where(Department.name_department == request.json['name'])
            except:
                return {}, 400
            else:
                department.execute()
                return {}, 200





api.add_resource(DepartmentApi, '/department')



if __name__ == '__main__':
    app.run(debug=True)