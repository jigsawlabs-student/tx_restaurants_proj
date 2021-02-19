import pytest
import psycopg2

from .context import api
from backend.src.models import City, Merchant, Zipcode, CityZipcode
from backend.src.orm import find_or_create
from backend.src.db import drop_all_tables


@pytest.fixture()
def city():
    drop_all_tables(conn, cursor)

    brooklyn = find_or_create(City(name='Brooklyn'), conn, cursor)[0]
    manhattan = find_or_create(City(name='Manhattan'), conn, cursor)[0]
    philadelphia = find_or_create(City(name='Philadelphia'), conn, cursor)[0]

    south_philly_zip = find_or_create(Zipcode(name='19019'), conn, cursor)[0]
    chelsea_zip = find_or_create(Zipcode(name='10001'), conn, cursor)[0]
    gramercy_zip = find_or_create(Zipcode(name='10010'), conn, cursor)[0]
    dumbo_zip = find_or_create(Zipcode(name='11210'), conn, cursor)[0]
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [find_or_create(Zipcode(name=z), conn, cursor)[0] for z in zips_list]

    for zipcode in brooklyn_zips:
        find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=zipcode.id), conn, cursor)[0]
    yield
    drop_all_tables(conn, cursor)

def test_zipcodes(city):
    pass
    # codes = [zipcode.name for zipcode in city.zipcodes(cursor)]
    # assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
