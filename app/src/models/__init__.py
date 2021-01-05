from .city import City
from .merchant import Merchant
from .zipcode import Zipcode
from .city_zipcode import CityZipcode
# from .db import *


## TODO: following is unused, but I'd like to.
def initialize_table(this, **kwargs):
    """
    Set up one of some class in models. Called in __init__s in all
    model class definitions.
    """
    print('initialize', this, type(this), kwargs)
    for key, value in kwargs.keys():
        if key not in this.columns:
            raise f'{key} not in {this.columns}' 
        setattr(this, key, value)
