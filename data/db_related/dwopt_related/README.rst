Set up a test postgres database::

    sudo su postgres
    psql
    CREATE DATABASE test_db;
    CREATE USER test_db_user WITH PASSWORD '1234';
    GRANT ALL PRIVILEGES ON DATABASE test_db to test_db_user;
    \q
    exit

