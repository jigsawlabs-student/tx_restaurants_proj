from flask import current_app
from flask import g
import psycopg2
import db.db_pass as pw

conn_dev = psycopg2.connect(database='jigsaw_project', user='postgres', password=pw.passwd)

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(user='postgres', password=passwd,
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

def find(This_class, id, cursor):
    sql_str = f"SELECT * FROM {This_class.__table__} WHERE id = %s"
    cursor.execute(sql_str, (id,))
    record = cursor.fetchone()
    return build_from_record(This_class, record)

def save(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
    venue_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str});"""
    cursor.execute(venue_str, list(values(obj)))
    conn.commit()
    cursor.execute(f'SELECT * FROM {obj.__table__} ORDER BY id DESC LIMIT 1')
    record = cursor.fetchone()
    return build_from_record(type(obj), record)

def values(obj):
    venue_attrs = obj.__dict__
    return [venue_attrs[attr] for attr in obj.columns if attr in venue_attrs.keys()]

def keys(obj):
    venue_attrs = obj.__dict__
    selected = [attr for attr in obj.columns if attr in venue_attrs.keys()]
    return ', '.join(selected)

def drop_records(cursor, conn, table_name):
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()
    # if I want to try to reset index on new ids to start at 1     ALTER SEQUENCE <table name>_id_seq RESTART;
    cursor.execute(f'')

def drop_tables(table_names, cursor, conn):
    for table_name in table_names:
        drop_records(cursor, conn, table_name)

def drop_all_tables(conn, cursor):
    table_names = ['', 'zipcodes', 'cities', 'retailers', 'cities_zips']
    drop_tables(table_names, cursor, conn)

def find_by_name(This_class, name, cursor):
    query = f"""SELECT * FROM {This_class.__table__} WHERE name = %s """
    cursor.execute(query, (name,))
    record =  cursor.fetchone()
    obj = build_from_record(This_class, record)
    return obj

def find_or_create_by_name(This_class, name, conn, cursor):
    obj = find_by_name(This_class, name, cursor)
    if not obj:
        new_obj = This_class()
        new_obj.name = name
        obj = save(new_obj, conn, cursor)
    return obj

def find_or_build_by_name(This_class, name, cursor):
    obj = This_class.find_by_name(name, cursor)
    if not obj:
        obj = This_class()
        obj.name = name
    return obj

