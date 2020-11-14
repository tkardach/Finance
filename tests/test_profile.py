import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
from mysql.connector import errorcode
from finance.config import Config
from finance.mysql import *
from finance.profile import *

test_email = 'test@email.com'
test_id = -1

def delete_all_profiles():
  # delete all created profiles
  cnx = get_connection()

  cursor = cnx.cursor()
  cursor.execute('DELETE FROM profile')
  cnx.commit()

  cursor.close()
  cnx.close()

class TestProfile(unittest.TestCase):
    def setUp(self):
      # must delete initially in case previous testing failed
      delete_all_profiles()
      create_profile(test_email, 'testpassword')
    
    def tearDown(self):
      delete_all_profiles()

    # get_profiles should return all profiles in database 
    def test_get_profiles(self):
      profiles = get_profiles()
      self.assertEqual(len(profiles), 1)
      self.assertEqual(profiles[0][1], test_email)
      
    # create_profile should add a new row to the profile table in the database
    def test_create_profile(self):
      raises = False
      try:
        new_email = 'create@profile.com'
        create_profile(new_email, 'testpassword')
      except:
        raises = True

      self.assertFalse(raises)

      profiles = get_profiles()
      self.assertEqual(len(profiles), 2)

    # create_profile should not add a new profile if email already exists
    def test_create_profile_duplicate_email(self):
      raises = False
      try:
        ret = create_profile(test_email, 'testpassword')
      except mysql.connector.Error as err:
        raises = True
      self.assertTrue(raises)

      profiles = get_profiles()
      self.assertEqual(len(profiles), 1)

    # get_profile should return the profile given the profile id
    def test_get_profile(self):
      profile_id = get_profile_id(test_email)
      self.assertIsNotNone(profile_id)
      profile = get_profile(profile_id)
      self.assertIsNotNone(profile)
      self.assertEqual(test_email, profile[1])

    # get_profile should return the None given the profile id is not in database
    def test_get_profile(self):
      profile_id = get_profile_id('does_not_exist')
      self.assertIsNone(profile_id)

    # get_profile_id should return the id of the profile given the profile email
    def test_get_profile_id(self):
      profile_id = get_profile_id(test_email)
      self.assertIsNotNone(profile_id)

    # get_profile_id should return None if there is no profile with the given email
    def test_get_profile_id(self):
      profile_id = get_profile_id('notindb@fail.com')
      self.assertIsNone(profile_id)