import unittest
import tests
from finance.database.database import engine, SessionLocal
from finance.utility.security import *
from finance.database.models import User, Role
from finance.database.user import *

class TestORMUser(unittest.TestCase):
  session = None
  test_name = 'test_user'
  test_email = 'test@email.com'
  test_is_admin = True
  test_password = 'mytestpassword'

  def delete_all_rows(self):
    self.session.query(Role).delete()
    self.session.query(User).delete()
    self.session.commit()


  def setUp(self):
    self.session = SessionLocal()
    self.delete_all_rows()
  
  def tearDown(self):
    self.delete_all_rows()
    self.session.close()

  def test_create_user(self):
    raises = False
    try:
      prof = create_user(
        self.session,
        self.test_email,
        self.test_password,
        self.test_is_admin
      )
      self.session.commit()
    except:
      self.session.rollback()
      raises = True

    self.assertFalse(raises)
    self.assertEqual(len(self.session.query(User).all()), 1)
    self.assertEqual(prof.email, self.test_email)
    self.assertEqual(prof.is_admin, self.test_is_admin)
    self.assertTrue(check_hashed_string(self.test_password, prof.password))


  def test_get_users(self):
    new_user_2 = 'new@user.com'
    raises = False
    try:
      prof1 = create_user(
        self.session,
        self.test_email,
        self.test_password,
        self.test_is_admin
      )
      prof2 = create_user(
        self.session,
        new_user_2,
        self.test_password,
        self.test_is_admin
      )
      self.session.commit()
      profs = get_users(self.session)
    except:
      raises = True

    self.assertFalse(raises)
    self.assertEqual(len(profs), 2)
    self.assertTrue(prof1 in profs)
    self.assertTrue(prof2 in profs)


  def test_get_user_by_email(self):
    raises = False
    try:
      created_prof = create_user(
        self.session,
        self.test_email,
        self.test_password,
        self.test_is_admin
      )
      self.session.commit()
      queried_prof = get_user_by_email(self.session, self.test_email)
    except:
      raises = True

    self.assertFalse(raises)
    self.assertEqual(created_prof, queried_prof)


  def test_get_user_by_id(self):
    raises = False
    try:
      created_prof = create_user(
        self.session,
        self.test_email,
        self.test_password,
        self.test_is_admin
      )
      self.session.commit()
      by_email = get_user_by_email(self.session, self.test_email)
      queried_prof = get_user_by_id(self.session, by_email.user_id)
    except:
      raises = True

    self.assertFalse(raises)
    self.assertEqual(created_prof, queried_prof)