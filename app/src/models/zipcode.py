from src import db
from src import models

class Zipcode(models.Table):
    __table__ = 'zipcodes'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        Merchant.initialize_table(kwargs)

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
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return db.build_from_records(models.Merchant, records)
