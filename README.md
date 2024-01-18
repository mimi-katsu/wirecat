Data base migrations

migrations are to be managed using "Alembic" python package.

Install: 
    pip install alembic

Initialize:
    In Top level of app:
        -run "alembic init alembic"
        -This should create a "alembic.ini" file (in the direcotry the command was run) 
            and a folder named "alembic" that contains and "env.py" file and "versions" directory.

Config:
    -In "alembic.ini":
        -"sqlalchemy.url = driver://user:pass@localhost/dbname" should be modified to 
            represent the actula databse url(Ex: sqlite:///instance/wirecat.sqlite)

    -In "alembic/env.py":
        - Import Base from db models file:
            -"from db import Base"
        -"target_metadata = None" should be changed to:
            - "target_metadata = Base.metadata"

Usage:
    - Always Backup DB before migrating!!!
    - Run "alembic revision --autogenerate -m 'Description of changes'" to create the migration 
        script in "alembic/versions/"

    - Run "alembic upgrade head" to start the migration

    - Run "alembic downgrade -1" to rollback to the last version.

.gitignore:
    alembic.ini
    alembic/
