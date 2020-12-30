import pytest
from flask import json
from jigsaw_project.app.models import Zipcode, City
from app.db import close_db, get_db, passwd, save


test_conn = psycopg2.connect(database = 'jigsaw_project_test', user = 'postgres', password = db.passwd)
test_cursor = test_conn.cursor()


# @pytest.fixture
# def test_city_zipcode():

