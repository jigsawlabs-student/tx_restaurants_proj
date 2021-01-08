from src import models

class CityZipcode(models.Table):
    __table__ = 'cities_zipcodes'
    columns = ['id', 'city_id', 'zip_id']

    def __init__(self, **kwargs):
        CityZipcode.initialize_table(kwargs)

