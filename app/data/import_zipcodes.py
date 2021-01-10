import psycopg2
import csv

from models import Areacode, City, Zipcode
from src import db


# TODO: import area codes
# with 

# import zips and cities
with open('zipcodes.csv') as z:
    zipcodes = csv.DictReader(z, delimiter=',', quotechar='"')
    for zipcode in zipcodes:
        if zipcode['zipcode']:
            new_zip = db.find_or_create(Zipcode(name=zipcode['zip']), db.conn, db.cursor)
            new_city = db.find_or_create(City(name=zipcode['primary_city']), db.conn, db.cursor)
            cross = db.find_or_create(CityZipcode(city_id=new_city.id, zip_id=new_zip.id), db.conn, db.cursor)
            if zipcode['acceptable_cities']:
                for city in split(zipcode['acceptable_cities']):
                    new_city = db.find_or_create(City(name=zipcode['acceptable_cities']), db.conn, db.cursor)
                    cross = db.find_or_create(CityZipcode(city_id=new_city.id, zip_id=new_zip.id), db.conn, db.cursor)
