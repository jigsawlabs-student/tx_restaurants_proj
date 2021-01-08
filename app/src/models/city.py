from src import db
from src import models

class City:
    __table__ = 'cities'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        # app.src.models.initialize_table(kwargs)
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
            setattr(self, key, kwargs[key])

    @classmethod
    def find_by_name(cls, name):
        """
        Return a City object with all fields for any record that matches the 
        name of the input object.
        """
        query_str = ('SELECT * '
                       'FROM %s'
                      'WHERE name = %s'
                    )
        cursor.execute(query_str, (cls.__table__,name))
        record = cursor.fetchone()
        return db.build_from_record(cls, record)


    def zipcodes(self, cursor):
        """Return all zip codes in this city."""
        query_str = ('SELECT z.name '
                       'FROM zipcodes z '
                       'JOIN cities_zipcodes cz '
                         'ON cz.zip_id = z.id '
                      'WHERE cz.city_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Zipcode, records)


    def merchants(self, cursor):
        """Return all merchants in this city."""
        query_str = ('SELECT m.* '
                       'FROM merchants m JOIN cities_zipcodes cz '
                         'ON m.cz_id = cz.id '
                      'WHERE cz.city_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Merchant, records)

