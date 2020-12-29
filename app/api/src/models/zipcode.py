import db
import models

class Zipcode:
    __table__ = 'zipcodes'
    columns = ['id', 'code', 'city_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_code(self, zip_code, cursor):
        query = f'SELECT * FROM {self.__table__} WHERE zip = %s '
        cursor.execute(query, (zip_code,))
        record =  cursor.fetchone()
        obj = db.build_from_record(self, record)
        return obj

    def cities(self, cursor):
        query_str = "SELECT cities.* FROM cities WHERE id = %s"
        cursor.execute(query_str, (self.zip_id,))
        records = cursor.fetchall()
        return db.build_from_records(models.City, records)

    def retailers(self, cursor):
        query = ('')
