import pytest
from decimal import *

from .context import api
from api.src.models import City, CityZipcode, Merchant, Zipcode
from api.src.db import cursor, conn, drop_all_tables, find_or_create

@pytest.fixture()
def build_cities():
    drop_all_tables(conn, cursor)
    city = City()
    city.name = 'Brooklyn'
    find_or_create(city, conn, cursor)

    city = City()
    city.name = 'Manhattan'
    find_or_create(city, conn, cursor)
    yield

    drop_all_tables(conn, cursor)

def test_find_all(build_cities):
    categories = find_all(city, cursor)
    assert [city.name for city in cities] == ['Brooklyn', 'Manhattan']
