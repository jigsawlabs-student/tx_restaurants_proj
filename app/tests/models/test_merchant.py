import pytest
import psycopg2
from api.src.models import City, CityZipcode, Merchant, Zipcode
from api.src.db import drop_all_tables, find_or_create, conn, cursor


@pytest.fixture()
def city():
    drop_all_tables(test_conn, test_cursor)

    brooklyn = save(City(name='Brooklyn'), test_conn, test_cursor)
    manhattan = save(City(name='Manhattan'), test_conn, test_cursor)
    philadelphia = save(City(name='Philadelphia'), test_conn, test_cursor)

    south_philly_zip = save(Zipcode(code=19019), test_conn, test_cursor)
    chelsea_zip = save(Zipcode(code=10001), test_conn, test_cursor)
    gramercy_zip = save(Zipcode(code=10010), test_conn, test_cursor)
    dumbo_zip = save(Zipcode(code=11210), test_conn, test_cursor)
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [save(Zipcode(code=z), test_conn, test_cursor)[0] for z in zips_list]

    for zipcode in brooklyn_zips:
        save(CityZipcode(city_id=brooklyn.id, zipcode=zipcode.zip), test_conn, test_cursor)
    yield city
    drop_all_tables(test_conn, test_cursor)

def test_city_multiple_zipcodes(city):
    codes = [zipcode.code for zipcode in city.zipcodes(test_cursor)]
    assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
