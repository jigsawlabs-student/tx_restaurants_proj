from distutils import util
from flask import Flask, request
import simplejson as json
# from .db import get_db
from .models import City, CityZipcode, Zipcode

from .db import *
# from .adaptors import *

from dotenv import load_dotenv

load_dotenv()

TESTING = bool(util.strtobool(os.environ.get('TESTING')))
DEBUGGING = bool(util.strtobool(os.environ.get('DEBUGGING')))

db_name = os.environ.get('DB_NAME')
if TESTING:
    db_name += '_test'
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PASS')


def create_app(database='jigsaw_project_test', testing = TESTING, debug = DEBUGGING):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = database, DEBUG = debug, TESTING = testing)

    @app.route('/')
    def root_url():
        return 'Welcome to my api'

    @app.route('/city/<name>')
    def city(name):
        conn = db.get_db()
        cursor = conn.cursor()
        city = db.find_by_name(models.City, name, cursor)
        return json.dumps(city.__dict__['name'], default=str)

    @app.route('/cities')
    def cities():
        conn = db.get_db()
        cursor = conn.cursor()
        cities = db.find_all(models.City, cursor)
        city_names = [city.__dict__['name'] for city in cities]
        return json.dumps(city_names, default=str)

    @app.route('/cities/search')
    def search_cities():
        conn = db.get_db()
        cursor = conn.cursor()

        params = dict(request.args)
        cities = models.city.search(params, cursor)
        city_dicts = [city.to_json(cursor) for city in cities]
        return json.dumps(city_dicts, default = str)

    @app.route('/city_zips/<name>')
    def city_zips(name):
        conn = db.get_db()
        cursor = conn.cursor()
        zipcodes = find_by_name(City, name, cursor).zipcodes(cursor)
        print(zipcodes)
        zipcode_names = [zipcode.__dict__['name'] for zipcode in zipcodes]
        return json.dumps(zipcode_names, default = str)

    @app.route('/zipcodes')
    def zipcodes():
        conn = db.get_db()
        cursor = conn.cursor()

        zipcodes = db.find_all(models.Zipcode, cursor)
        zipcode_dicts = [zipcode.__dict__['name'] for zipcode in zipcodes]
        return json.dumps(zipcode_dicts, default=str)

    # @app.route('/cities_by_zip/<id>')
    # def cities():
    #     conn = db.get_db()
    #     cursor = conn.cursor()

    #     cities = db.find_all(models.City, cursor)
    #     city_dicts = [city.__dict__['name'] for city in cities]
    #     return json.dumps(city_dicts, default=str)

    return app


