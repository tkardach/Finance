from urllib.parse import quote_plus as urlquote
from finance.utility.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://%s:%s@%s/%s' % (
  Config.db_user, 
  urlquote(Config.db_pass),
  Config.db_host,
  Config.db_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
