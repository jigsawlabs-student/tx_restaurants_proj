import psycopg2
from src.models import City, Merchant, Zipcode, CityZipcode
from src.db import *


drop_all_tables(conn, cursor)

def build_city_zipcode(city_name = '', zipcode = ''):
    """Create data for testing of tables."""
    if city_name and zipcode:
        zipcode = find_or_create(Zipcode(name=zipcode), conn, cursor)[0]
        city = find_or_create(City(name=city_name), conn, cursor)[0]
        cross = find_or_create(CityZipcode(city_id=city.id, zip_id=zipcode.id), conn, cursor)
    return city, zipcode, cross

manhattan_zip = build_city_zipcode('Manhattan', '10001')
_, ps_zip, _ = build_city_zipcode('Park Slope', '11220')
_, bh_zip, _ = build_city_zipcode('Brooklyn Heights', '11201')
_, ch_zip, _ = build_city_zipcode('Cobble Hill', '11201')
_, cg_zip, _ = build_city_zipcode('Carroll Gardens', '11213')

brooklyn, _, _ = build_city_zipcode('Brooklyn', ps_zip.name)
brooklyn2, _, _ = build_city_zipcode('Brooklyn', bh_zip.name)
brooklyn3, _, _ = build_city_zipcode('Brooklyn', cg_zip.name)
brooklyn4, _, _ = build_city_zipcode('Brooklyn', ch_zip.name)

# find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=brooklyn.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=brooklyn2.id, zip_id=brooklyn2.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=brooklyn3.id, zip_id=brooklyn3.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=brooklyn4.id, zip_id=brooklyn4.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=manhattan.id, zip_id=manhattan.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=park_slope.id, zip_id=park_slope.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=brooklyn_heights.id, zip_id=brooklyn_heights.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=cobble_hill.id, zip_id=cobble_hill.zipcode), conn, cursor)
# find_or_create(CityZipcode(city_id=carroll_gardens.id, zip_id=carroll_gardens.zipcode), conn, cursor)


