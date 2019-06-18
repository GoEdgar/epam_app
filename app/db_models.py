import configparser

from peewee import *


config = configparser.ConfigParser()
config.read('../config.ini')

params_for_db = {'host': config['db']['host'],
                 'user': config['db']['user'],
                 'password': config['db']['password'],
                 'database': config['db']['database']}

#if is test
test_database = config['db']['test_database']
if test_database:
    params_for_db['database'] = test_database

db = PostgresqlDatabase(**params_for_db)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

class Department(BaseModel):
    name_department = CharField(unique=True)

class Employee(BaseModel):
    name_department = ForeignKeyField(Department, field='name_department')
    full_name = CharField()
    date_of_brith = DateTimeField()
    salary = IntegerField()




if __name__ == '__main__' or config:
    db.drop_tables([Department, Employee])
    db.create_tables([Department, Employee])
