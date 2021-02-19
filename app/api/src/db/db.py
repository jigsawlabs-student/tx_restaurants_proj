from flask import current_app, g
import psycopg2
import os
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()

db_name = os.environ.get('DB_NAME')
if strtobool(os.environ.get('TESTING')):
    db_name += '_test'
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PASS')
# TODO: see line 26. Could/should do this in fixture instead, for eventual Flask testing.
# ^^^ huh? line 26? ^^^
# TODO: Parts of this could/should be moved to orm.py, no?

TABLES = ['areacodes', 'zipcodes', 'cities', 'merchants', 'areacodes_zipcodes', 'cities_zipcodes']

conn = psycopg2.connect(database=db_name, user=db_user, password=db_pw)
cursor = conn.cursor()

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(user=db_user, password=db_pw,
            dbname = current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def build_from_record(This_class, record):
    if not record: return None
    attr = dict(zip(This_class.columns, record))
    obj = This_class()
    obj.__dict__ = attr
    return obj

def build_from_records(This_class, records):
   return [build_from_record(This_class, record) for record in records]

def find_all(This_class, cursor):
    sql_str = f"SELECT * FROM {This_class.__table__}"
    cursor.execute(sql_str)
    records = cursor.fetchall()
    return [build_from_record(This_class, record) for record in records]

def find_by_id(This_class, id, cursor):
    """
    Retrieve record by id from DB, create and return obj of type This_class
    with values from that record.
    """
    sql_str = f"SELECT * FROM {This_class.__table__} WHERE id = %s"
    cursor.execute(sql_str, (id,))
    record = cursor.fetchone()
    return build_from_record(This_class, record)

def find_by_name(This_class, name, cursor):
    """
    Retrieve record by name from DB, create and return obj of type This_class
    with values from that record.
    """
    sql_str = f"SELECT * FROM {This_class.__table__} WHERE name = %s"
    cursor.execute(sql_str, (name,))
    record = cursor.fetchone()
    return build_from_record(This_class, record)


# JK: Instead of exception for non unique, is it possible to only create if does not exist.  
# Generally, try to avoid exceptions and rollbacks, so would continue to look for other ways to avoid.
def find_or_create(obj, conn, cursor):
    """Save values in input obj into DB. Return a *list* of *new* objects of same type."""
    values_str = ', '.join(len(values(obj)) * ['%s'])
    keys_str = ', '.join(keys(obj))
    insert_str = f'INSERT INTO {obj.__table__} ({keys_str}) VALUES ({values_str});'
    try:
        cursor.execute(insert_str, list(values(obj)))
        conn.commit()
        cursor.execute(f'SELECT * FROM {obj.__table__} ORDER BY id DESC LIMIT 1')
    except Exception as e: # Need to have exception for unique fields. Must do SELECT after insertion. 
                           # Doing SELECT first would return values already inserted for non-unique fields.
        condition_str = ' WHERE '
        for k in keys(obj):
            condition_str += k + ' = %s AND '
        condition_str = condition_str[:-5]
        cursor.execute('ROLLBACK')
        cursor.execute('SELECT * FROM ' + obj.__table__ + condition_str, tuple(values(obj)))
    records = cursor.fetchall()     # fetchall() and not fetchone() in case of non-unique fields
    result = build_from_records(type(obj), records)
    return result

def values(obj):
    """Return a list of values from the __dict__ in obj."""
    obj_attrs = obj.__dict__
    return [obj_attrs[attr] for attr in obj.columns if attr in obj_attrs.keys()]

def keys(obj):
    """Return a list of values from the __dict__ ;in obj."""
    obj_attrs = obj.__dict__
    return [attr for attr in obj.columns if attr in obj_attrs.keys()]

def drop_records(table_name, cursor, conn):
    """Drop all records from table_name."""
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

def drop_tables(table_names, cursor, conn):
    """Drop tables in input list table_names."""
    for table_name in table_names:
        drop_records(table_name, cursor, conn)

def drop_all_tables(conn, cursor):
    table_names = TABLES
    drop_tables(table_names, cursor, conn)
