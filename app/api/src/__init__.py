from distutils import util
from dotenv import load_dotenv
from flask import Flask, request
import simplejson as json
import os

from api.src.db import find_all, find_by_name, get_db
from api.src.models import Areacode, City, CityZipcode, Merchant, Table, Zipcode

# from .adaptors import *


load_dotenv()

TESTING = bool(util.strtobool(os.environ.get('TESTING')))
DEBUGGING = bool(util.strtobool(os.environ.get('DEBUGGING')))

db_name = os.environ.get('DB_NAME')
if TESTING:
    db_name += '_test'
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PASS')

# TODO: What information should I "surface" on, say, city? 
# Should I list restaurants and zip, for instance?
# In that case, I could remove zip_and_city_of_merchant().

def create_app(database='jigsaw_project_test', testing = TESTING, debug = DEBUGGING):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = database, DEBUG = debug, TESTING = testing)

    @app.route('/')
    def root_url():
        return 'Welcome to my api'

    @app.route('/city/<city_name>')
    def city(city_name):
        """Return complete record for city with name == city_name."""
        conn = db.get_db()
        cursor = conn.cursor()
        city = db.find_by_name(models.City, city_name, cursor)
        return json.dumps(city.__dict__, default=str)

    @app.route('/cities')
    def cities():
        """Return complete records for all cities in DB."""
        conn = db.get_db()
        cursor = conn.cursor()
        cities = db.find_all(models.City, cursor)
        city_names = [city.__dict__ for city in cities]
        return json.dumps(city_names, default=str)

    # @app.route('/cities/search')
    # def search_cities():
    #     conn = db.get_db()
    #     cursor = conn.cursor()

    #     params = dict(request.args)
    #     cities = models.city.search(params, cursor)
    #     city_dicts = [city.to_json(cursor) for city in cities]
    #     return json.dumps(city_dicts, default = str)

    @app.route('/zips_for_city/<city_name>')
    def zips_for_city(city_name):
        """
        For a city given by city_name, return complete record for all 
        zipcodes in that city.
        """
        conn = db.get_db()
        cursor = conn.cursor()
        zipcodes = db.find_by_name(City, city_name, cursor).zipcodes(cursor)
        print(zipcodes)
        zipcode_names = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_names, default = str)

    @app.route('/zipcodes')
    def zipcodes():
        """Return all zipcodes in DB."""
        conn = db.get_db()
        cursor = conn.cursor()

        zipcodes = db.find_all(models.Zipcode, cursor)
        zipcode_dicts = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_dicts, default=str)

    @app.route('/cities_for_zip/<zipcode>')
    def cities_for_zip(zipcode):
        """ For a zip with name zipcode, return all cities in that zipcode."""
        conn = db.get_db()
        cursor = conn.cursor()

        cities = db.find_by_name(Zipcode, zipcode, cursor).cities(cursor)
        city_dicts = [city.__dict__ for city in cities]
        return json.dumps(city_dicts, default=str)

    @app.route('/merchants')
    def merchants():
        """Return all merchants in DB."""
        conn = db.get_db()
        cursor = conn.cursor()

        merchants = db.find_all(models.Merchant, cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants_for_city/<city_name>')
    def merchants_for_city(city_name):
        """ For a city with name city_name, return all merchants in that city."""
        conn = db.get_db()
        cursor = conn.cursor()

        merchants = db.find_by_name(City, city_name, cursor).merchants(cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants_for_zip/<zipcode>')
    def merchants_for_zip(zipcode):
        """ For a zip with name zipcode, return all merchants in that zipcode."""
        conn = db.get_db()
        cursor = conn.cursor()
        merchants = db.find_by_name(Zipcode, zipcode, cursor).merchants(cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/zip_and_city_of_merchant/<merchant_name>')
    def zip_and_city_of_merchant(merchant_name):
        """ For a merchant with name merchant_name, return its zipcode and city."""
        conn = db.get_db()
        cursor = conn.cursor()

        merchant = db.find_by_name(Merchant, merchant_name, cursor)
        zipcode = merchant.zipcode(cursor)
        city = merchant.city(cursor)
        merchant_dicts = [{'zipcode': zipcode.name, 'city': city.name}]
        return json.dumps(merchant_dicts, default=str)

    return app


