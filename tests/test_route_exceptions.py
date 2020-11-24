import unittest
import tests
import json
from finance.database.database import SessionLocal
from finance.database.models import User
from finance.server import app
from werkzeug.exceptions import InternalServerError


@app.route('/test', methods=['GET'])
def test_route():
    user = User('test_email@email.com', 'password', False)
    app.session.add(user)
    raise Exception('test')

class TestRouteExceptions(unittest.TestCase):
    session = None
    def call_test_route(self):
        return self.client.get('/test')
  
    def delete_all_rows(self):
        self.session.query(User).delete()
        self.session.commit()

    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.client = app.test_client()

    def tearDown(self):
        self.delete_all_rows()
        self.session.close()

    # we expect the session to rollback on exception call
    def test_exception_rollback(self):
        response = self.call_test_route()
        
        # try to commit any changes made in /test route
        app.session.commit()
        self.assertEqual(response.status_code, 500)

        # verify the session was rolled back after exception was caught
        self.assertEqual(len(self.session.query(User).all()), 0)
        
        