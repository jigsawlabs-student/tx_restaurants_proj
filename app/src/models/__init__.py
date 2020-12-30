from .zipcode import Zipcode
from .city import City
# from .db import *
from .db_pass import *

def initialize_table(this, **kwargs):
    for key in kwargs.keys():
        if key not in self.columns:
            raise f'{key} not in {self.columns}' 
    for k, v in kwargs.items():
        this.setattr(self, k, v)
