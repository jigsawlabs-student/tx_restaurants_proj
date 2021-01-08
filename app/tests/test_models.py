import pytest
import psycopg2
from src.models import City, Merchant, Zipcode
from app.src.db import close_db, get_db, db_pw, db_user, db_name, save, drop_all_tables


@pytest.fixture()
def city():
    drop_all_tables(conn, cursor)

    brooklyn = save(City(name='Brooklyn'), conn, cursor)
    manhattan = save(City(name='Manhattan'), conn, cursor)
    philadelphia = save(City(name='Philadelphia'), conn, cursor)

    south_philly_zip = save(Zipcode(code=19019), conn, cursor)
    chelsea_zip = save(Zipcode(code=10001), conn, cursor)
    gramercy_zip = save(Zipcode(code=10010), conn, cursor)
    dumbo_zip = save(Zipcode(code=11210), conn, cursor)
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [save(Zipcode(code=z), conn, cursor) for z in zips_list]

    for zipcode in brooklyn_zips:
        save(CityZipcode(city_id=brooklyn.id, zipcode=zipcode.zip), conn, cursor)
    yield
    drop_all_tables(conn, cursor)

def test_zipcodes(city):
    codes = [zipcode.code for zipcode in city.zipcodes(cursor)]
    assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
