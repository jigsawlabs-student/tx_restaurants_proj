1. Table.py
Nice use of inheritance there.  
I think you need a call to `super` to get it working for the init function.
It's fine to move the orm functions there if you prefer (I have no preference).
ActiveRecord from rails uses an inheritance pattern, while sqlalchemy uses more of the pattern in our orm.py file.

2. Don't be afraid of the frontend.  

3. Look at my pattern for manage.py in the add_cli branch.  Use instead of run.py and run_adapters.py


TODO:
A. Work on the adapters.
B.  You did a lot of the setup for tests, so now it's time to write some.  
C. To build on your project, you can add aggregate functions.  
# Think about what you want to return from the frontend, and go from there.

Overall, obvious that you put a good degree of thought into the structure of the projects, and each method.  Still have tasks to complete.

