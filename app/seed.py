import psycopg2
from src import *


drop_all_tables(conn, cursor)

def build_city_zipcode(city_name = '', zipcode = ''):
    if city_name and zipcode:
        zipcode = find_or_create_by_name(Zipcode, zipcode, conn, cursor)
        city = find_or_create_by_name(City, city_name, conn, cursor)
    return city, zipcode

manhattan = build_city_zipcode('Manhattan', '10001')
park_slope = build_city_zipcode('Park Slope', '11220')
brooklyn_heights = build_city_zipcode('Brooklyn Heights', '11201')
cobble_hill = build_city_zipcode('Cobble Hill', '11201')
carroll_gardens = build_city_zipcode('Carroll Gardens', '11213')

brooklyn = build_city_zipcode('Brooklyn', park_slope.zipcode)
brooklyn2 = build_city_zipcode('Brooklyn', brooklyn_heights.zipcode)
brooklyn3 = build_city_zipcode('Brooklyn', cobble_hill.zipcode)
brooklyn4 = build_city_zipcode('Brooklyn', carroll_gardens.zipcode)

save(CityZipcode(city_id=brooklyn.id, zip_id=brooklyn.zipcode))
save(CityZipcode(city_id=brooklyn2.id, zip_id=brooklyn2.zipcode))
save(CityZipcode(city_id=brooklyn3.id, zip_id=brooklyn3.zipcode))
save(CityZipcode(city_id=brooklyn4.id, zip_id=brooklyn4.zipcode))
save(CityZipcode(city_id=manhattan.id, zip_id=manhattan.zipcode))
save(CityZipcode(city_id=park_slope.id, zip_id=park_slope.zipcode))
save(CityZipcode(city_id=brooklyn_heights.id, zip_id=brooklyn_heights.zipcode))
save(CityZipcode(city_id=cobble_hill.id, zip_id=cobble_hill.zipcode))
save(CityZipcode(city_id=carroll_gardens.id, zip_id=carroll_gardens.zipcode))


