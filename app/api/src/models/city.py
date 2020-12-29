import db
import models

class City:
    __table__ = 'cities'
    columns  = ['id', 'name']

    def __init__(self, **kwargs):
        models.initialize_table(self, kwargs)


    @classmethod
    def get_from_name(cls):
        query_str = ('SELECT * FROM cities '
                      'WHERE name = '
                    )
        cursor.execute(query_str, (cls,))
        record = cursor.fetchone()
        return db.build_from_record(cls, record)


    def zipcodes(self, cursor):
        query_str = ('SELECT z.zip '
                       'FROM zipcodes z JOIN cities_zips cz '
                         'ON cz.zip_id = z.zip '
                      'WHERE cz.city_id = %s'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Zipcode, records)


    def retailers(self, cursor):
        query_str = ('SELECT r.name '
                        'FROM retailers r'
                       'WHERE r.city_id = %s'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Retailers, records)

