import pytest
import psycopg2
from .context import api
from api.src.models import City, CityZipcode, Merchant, Zipcode
from api.src.db import drop_all_tables, find_or_create, conn, cursor


@pytest.fixture()
def city():
    drop_all_tables(conn, cursor)

    brooklyn = find_or_create(City(name='Brooklyn'), conn, cursor)
    manhattan = find_or_create(City(name='Manhattan'), conn, cursor)
    philadelphia = find_or_create(City(name='Philadelphia'), conn, cursor)

    south_philly_zip = find_or_create(Zipcode(name=19019), conn, cursor)
    chelsea_zip = find_or_create(Zipcode(name=10001), conn, cursor)
    gramercy_zip = find_or_create(Zipcode(name=10010), conn, cursor)
    dumbo_zip = find_or_create(Zipcode(name=11210), conn, cursor)
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [find_or_create(Zipcode(name=z), conn, cursor)[0] for z in zips_list]

    for zipcode in brooklyn_zips:
        find_or_create(CityZipcode(city_id=brooklyn.id, zipcode=zipcode.zip), conn, cursor)
    yield city
    drop_all_tables(conn, cursor)

def test_city_multiple_zipcodes(city):
    codes = [zipcode.name for zipcode in city.zipcodes(cursor)]
    assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
