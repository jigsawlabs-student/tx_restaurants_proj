import pytest
from decimal import *
from app.src import *

@pytest.fixture()
def build_cities():
    drop_all_tables(test_conn, test_cursor)
    city = City()
    city.name = 'Brooklyn'
    save(city, test_conn, test_cursor)

    city = City()
    city.name = 'Manhattan'
    save(city, test_conn, test_cursor)
    yield

    drop_all_tables(test_conn, test_cursor)

def test_find_all(build_cities):
    categories = find_all(city, test_cursor)
    assert [city.name for city in cities] == ['Brooklyn', 'Manhattan']
