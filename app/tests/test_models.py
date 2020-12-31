import pytest
import psycopg2
from flask import json
from app.src.models import Zipcode, City
from app.src.db import close_db, get_db, db_pw, db_user, db_name, save


test_conn = psycopg2.connect(database = db_name, user = db_user, password = db_pw)
test_cursor = test_conn.cursor()


# @pytest.fixture
# def test_city_zipcode():

