from peewee import *

db = PostgresqlDatabase(database='postgres', user='postgres')
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




if __name__ == '__main__':
    db.drop_tables([Department, Employee])
    db.create_tables([Department, Employee])
