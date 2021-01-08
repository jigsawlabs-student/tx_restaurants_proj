import src.db
import src.models

class Merchant:
    __table__ = 'merchants'
    columns = ['id', 'name', 'cz_id', 'liquor_sales', 'beer_sales', 'wine_sales', 'cover_sales']

    def __init__(self, **kwargs):
        # app.src.models.initialize_table(kwargs)
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
            setattr(self, key, kwargs[key])

    @classmethod
    def find_by_name(cls, name, cursor):
        query = f'SELECT * FROM {self.__table__} WHERE name = %s;'
        cursor.execute(query, (name,))
        record =  cursor.fetchone()
        obj = db.build_from_record(self, record)
        return obj


    def city(self, cursor):
        """Return the city where this merchant is located."""
        query_str = ('SELECT c.* ',
                       'FROM cities c ',
                       'JOIN cities_zipcodes cz ON cz.city_id = c.id ',
                      'WHERE cz.id = %s;'
                    )
        cursor.execute(query_str, (self.city_zip_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.City, record)


    def zipcode(self, cursor):
        """Return the city where this merchant is located."""
        query_str = ('SELECT z.* ',
                       'FROM zipcodes z ',
                       'JOIN cities_zipcodes cz ON cz.city_id = c.id ',
                      'WHERE cz.id = %s;'
                    )
        cursor.execute(query_str, (self.city_zip_id,))
        record = cursor.fetchone()
        return db.build_from_record(models.Zipcode, record)
