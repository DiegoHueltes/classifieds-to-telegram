from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db import init_db
from settings import TEST_DB_PATH, os

test_engine = create_engine('sqlite:////{}'.format(TEST_DB_PATH))
Session = sessionmaker(bind=test_engine)
Base = declarative_base()
session = Session()


def init_tests():
    init_db(test_engine)


def teardown_tests():
    os.remove(TEST_DB_PATH)
