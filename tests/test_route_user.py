import unittest
import tests
import json
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.models import User, Role


class TestRouteUser(unittest.TestCase):
    test_email = 'test@user.com'
    test_pass = 'test_password'
    test_user = None
    session = None

    def create_test_user(self):
        self.test_user = create_user(
            session=self.session, email=self.test_email, password=self.test_pass)
        self.session.commit()

    def post_login(self, email: str, password: str):
        test_login = {
            'email': email,
            'password': password
        }
        return self.client.post(
            '/login',
            data=json.dumps(test_login),
            content_type='application/json')

    def get_logout(self):
        return self.client.get('/logout')

    def get_profile(self):
        return self.client.get('/profile')

    def delete_all_rows(self):
        self.session.query(Role).delete()
        self.session.query(User).delete()
        self.session.commit()

    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.create_test_user()
        self.client = app.test_client()

    def tearDown(self):
        self.delete_all_rows()
        self.session.close()

    def test_profile_path(self):
        response = self.post_login(self.test_email, self.test_pass)
        self.assertEqual(response.status_code, 200)

        response = self.get_profile()
        self.assertEqual(response.status_code, 200)

        user = json.loads(response.data)
        self.assertEqual(user['email'], self.test_email)

    def test_profile_path_401_on_not_logged_in(self):
        response = self.get_profile()
        self.assertEqual(response.status_code, 401)
        