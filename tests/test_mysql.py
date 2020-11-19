import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
import sqlalchemy as db
from finance.utility.config import Config
from finance.database.mysql import *

class TestMySQL(unittest.TestCase):
    def setUp(self):
      pass
    
    def tearDown(self):
      pass

    def test_mysql_login(self):
      raises = False
      try:
        cnx = get_connection()
      except:
        raises = True
      else:
        cnx.close()
      self.assertFalse(raises)
    

    def test_mysql_get_engine(self):
      raises = False
      try:
        engine = get_engine()
      except:
        raises = True
      self.assertFalse(raises)
      

    def test_mysql_connect_engine(self):
      engine = get_engine()
      with engine.connect() as connection:
        self.assertIsNotNone(connection)


    def test_mysql_db_other(self):
      engine = get_engine()
      with engine.connect() as connection:
        metadata = db.MetaData()
        census = db.Table('single_transaction', metadata, autoload=True, autoload_with=engine)
        print(census.columns.keys())