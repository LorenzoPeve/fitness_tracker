## Init Testing DB

- Delete schema
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA IF NOT EXISTS public;
```
- Migrate with `python manage.py migrate`
- Run `etl\init.py` script

