# Elog

Collect your error logs in any application. This is a Flask app and this *README.md* is still being updated.

## dev_db
This folder contains the exact same details as found under the `database` section in 
[docker-compose.yml](docker-compose.yml). The only exceptions are:
1. container_name('s) differ
2. dev_db('s) version has `ports` in place of `expose`: the ports allow one to connect through the `host` to the DB
3. type `make` while in the `dev_db` directory to be able to see the available commands

The whole essence of duplicate .yml file is to connect to the DB during the development, if need be.