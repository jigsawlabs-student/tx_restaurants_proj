1. Table.py
Nice use of inheritance there.  
I think you need a call to `super` to get it working for the init function.
It's fine to move the orm functions there if you prefer (I have no preference).
ActiveRecord from rails uses an inheritance pattern, while sqlalchemy uses more of the pattern in our orm.py file.

2. Look at my pattern for manage.py in the add_cli branch.  Use instead of run.py and run_adapters.py


TODO:
A. Add  in the client  for the adapter pattern.
B. To build on your project, you can add aggregate functions.  
C. In your orm, looks like find_or_create returns a list.  Instead have it just return one object - this way you won't have to do find_or_create()[0] when you call it.

