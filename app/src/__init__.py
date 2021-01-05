from flask import Flask
from distutils import util
import simplejson as json
# from flask import request

from .models import *
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


def create_app(database='jigsaw-project_dev', testing = TESTING, debug = DEBUGGING):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = database, DEBUG = debug, TESTING = testing)

    @app.route('/')
    def root_url():
        return 'Welcome to my api'

    @app.route('/cities')
    def cities():
        conn = db.get_db()
        cursor = conn.cursor()

        cities = db.find_all(models.city, cursor)
        city_dicts = [city.__dict__ for city in cities]
        return json.dumps(city_dicts, default = str)

    @app.route('/cities/search')
    def search_cities():
        conn = db.get_db()
        cursor = conn.cursor()

        params = dict(request.args)
        cities = models.city.search(params, cursor)
        city_dicts = [city.to_json(cursor) for city in cities]
        return json.dumps(city_dicts, default = str)

    @app.route('/cities/<id>')
    def city(id):
        conn = db.get_db()
        cursor = conn.cursor()
        city = db.find(models.city, id, cursor)

        return json.dumps(city.__dict__, default = str)


    return app


