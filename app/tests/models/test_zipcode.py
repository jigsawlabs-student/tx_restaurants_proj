import pytest
import psycopg2
from app.src.models import City, CityZipcode, Merchant, Zipcode
from app.src.db import close_db, get_db, db_pw, db_user, db_name, save, drop_all_tables


conn = psycopg2.connect(database = db_name, user = db_user, password = db_pw)
cursor = conn.cursor()

@pytest.fixture()
def city():
    """
    Build a set of Citys, Zipcodes and Merchants in order to test that constructors
    and accessors are working correctly in model.
    """
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
        save(CityZipcode(city_id=brooklyn.id, zip_id=zipcode.id), conn, cursor)
    yield
    drop_all_tables(conn, cursor)

def test_zipcodes(city):
    codes = [zipcode.code for zipcode in city.zipcodes(cursor)]
    assert codes == [10001, 10010]


def test_city(city):
    city = City()

