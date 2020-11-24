import unittest
import tests
import json
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.models import User


class TestRouteAuth(unittest.TestCase):
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

    def post_signup(self, email: str, password: str):
        test_signup = {
            'email': email,
            'password': password
        }
        return self.client.post(
            '/signup',
            data=json.dumps(test_signup),
            content_type='application/json')

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

    def test_login_path(self):
        self.create_test_user()
        response = self.post_login(self.test_email, self.test_pass)
        self.assertEqual(response.status_code, 200)
        
    def test_login_400_on_missing_email(self):
        test_login = {
            'password': self.test_pass
        }
        response = self.client.post(
            '/login',
            data=json.dumps(test_login),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
    def test_login_400_on_missing_password(self):
        test_login = {
            'email': self.test_email
        }
        response = self.client.post(
            '/login',
            data=json.dumps(test_login),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_login_path_400_on_invalid_email(self):
        response = self.post_login('invalid.com', 'wrong')

        self.assertEqual(response.status_code, 400)

    def test_login_path_401_on_bad_password(self):
        self.create_test_user()
        response = self.post_login(self.test_email, 'wrong')

        self.assertEqual(response.status_code, 401)

    def test_login_path_401_on_wrong_email(self):
        self.create_test_user()
        response = self.post_login('not_in_db@email.com', self.test_pass)

        self.assertEqual(response.status_code, 401)

    def test_login_path_401_on_no_user(self):
        response = self.post_login(self.test_email, self.test_pass)

        self.assertEqual(response.status_code, 401)

    def test_login_path_400_on_bad_mimetype(self):
        response = self.client.post(
            '/login',
            data='{"email":"%s","password":"%s"}' % (self.test_email, self.test_pass),
            content_type='text/plain')

        self.assertEqual(response.status_code, 400)
        
    def test_signup(self):
        response = self.post_signup(self.test_email, self.test_pass)

        users = self.session.query(User).all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 1)

        user = users[0]
        self.assertEqual(user.email, self.test_email)
        
    def test_signup_400_on_user_exists(self):
        self.create_test_user()
        response = self.post_signup(self.test_email, self.test_pass)
        
        self.assertEqual(response.status_code, 400)
        
    def test_signup_400_on_missing_email(self):
        test_signup = {
            'password': self.test_pass
        }
        response = self.client.post(
            '/signup',
            data=json.dumps(test_signup),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
    def test_signup_400_on_missing_password(self):
        test_signup = {
            'email': self.test_email
        }
        response = self.client.post(
            '/signup',
            data=json.dumps(test_signup),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
    def test_signup_400_on_invalid_email(self):
        response = self.post_signup('email.com', self.test_pass)
        
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        self.create_test_user()
        response = self.post_login(self.test_email, self.test_pass)
        self.assertEqual(response.status_code, 200)

        response = self.get_logout()
        self.assertEqual(response.status_code, 200)

    def test_logout_401_on_user_not_logged_in(self):
        response = self.get_logout()
        self.assertEqual(response.status_code, 401)

