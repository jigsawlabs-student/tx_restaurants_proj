from src import db
from src import models

class Zipcode:
    __table__ = 'zipcodes'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        # app.src.models.initialize_table(kwargs)
        for key in kwargs.keys():
            if key not in self.columns:
                raise Exception(f'{key} not in {self.columns}')
            setattr(self, key, kwargs[key])

    @classmethod
    def find_by_zipcode(cls, zip_code, cursor):
        """
        Return a Zipcode object with all fields for any record that matches the 
        zipcode (coded as name) of the input object.
        """
        query = f'SELECT * FROM {self.__table__} WHERE name = %s;'
        cursor.execute(query, (zip_code,))
        record =  cursor.fetchone()
        obj = db.build_from_record(self, record)
        return obj

    def cities(self, cursor):
        """Return all cities in this zip code."""
        query_str = ('SELECT c.* '
                       'FROM cities c '
                       'JOIN cities_zipcodes cz ON cz.city_id = c.id '
                      'WHERE cz.zip_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.City, records)

    def merchants(self, cursor):
        """Return all merchants in this zip code."""
        query_str = ('SELECT m.* '
                       'FROM merchants m '
                       'JOIN cities_zipcodes cz ON m.cz_id = cz.id '
                      'WHERE cz.zip_id = %s;'
                    )
        cursor.execute(query_str, (self.name,))
        records = cursor.fetchall()
        return db.build_from_records(models.Merchant, records)
