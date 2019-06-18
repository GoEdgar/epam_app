import unittest
import psycopg2
import configparser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.config = config = configparser.ConfigParser()
        config.read('../config.ini')
        
        # write test config
        config['db']['test_database'] = 'test_epam_app'
        
        with open('../config.ini', 'w') as f:
            config.write(f)

        params_for_db = {'host': config['db']['host'],
                         'user': config['db']['user'],
                         'password': config['db']['password'],
                         'database': config['db']['database']}
        

        # create test DB
        with psycopg2.connect(**params_for_db) as connect:
            connect.set_isolation_level(0)
            with connect.cursor() as cursor:
                try:
                    cursor.execute('drop database test_epam_app')
                finally:
                    cursor.execute('create database test_epam_app')
                    
            
        from app.main import app
        app.testing = True
        self.app = app.test_client()
    
    def tearDown(self):
        self.config['db']['test_database'] = ''
        with open('../config.ini', 'w') as f:
            self.config.write(f)

    def test_home(self):
        result = self.app.get('/department')
        print(type(result))
                
unittest.main()
