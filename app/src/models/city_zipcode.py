# TODO: remove imports?
import src.db
from src import models as models

class CityZipcode:
    __table__ = 'cities_zipcodes'
    columns = ['id', 'city_id', 'zip_id']

    def __init__(self, **kwargs):
        # app.src.models.initialize_table(kwargs)
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
            setattr(self, key, kwargs[key])

