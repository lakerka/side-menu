# side-menu


Default database is PostgreSQL and it was set up according to [tutorial](https://docs.djangoproject.com/en/2.0/ref/databases/#postgresql-notes).
To setup database one should use `db_setup.sql` file instructions.


To run unit tests:
python manage.py test --noinput --keepdb

To delete tree nodes:
python manage.py delete_tree_nodes

To generate tree nodes:
python manage.py generate_tree
