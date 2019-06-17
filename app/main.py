from flask import Flask, request
from flask_restful import Api, Resource

from app.db_models import *

app = Flask(__name__)
api = Api(app)




class DepartmentApi(Resource):
    def get(self):
        departments = Department.select('name_department')
        return {'data':[dep for dep in departments]}, 200
    
    def post(self):
        if request.content_type == 'application/json':
            print(request.json)
            try:
                department = Department.create(**request.json)
            except IntegrityError:
                return {}, 409
            else:
                department.save()
                return {'data': request.json}





api.add_resource(DepartmentApi, '/department')



if __name__ == '__main__':
    app.run(debug=True)