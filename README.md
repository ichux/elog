# Elog

Collect your error logs in any application. This is a Flask app and this *README.md* is still being updated.

## dev_db
This folder contains the exact same details as found under the `database` section in 
[docker-compose.yml](docker-compose.yml). The only exceptions are:
1. container_name('s) differ
2. dev_db('s) version has `ports` in place of `expose`: the ports allow one to connect through the `host` to the DB
3. type `make` while in the `dev_db` directory to be able to see the available commands

The whole essence of a duplicate .yml file is to connect to the DB through a GUI during development, if need be.
However, if you want to connect to the DB through a shell, follow the steps outlined below. DO note that for this to 
have happened, `POSTGRES_DB` and `POSTGRES_USER` need to be of the same value.

a:
> docker-compose run --rm database psql -U elog --dbname elog -W -h $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' elog_psql)

b:
> enter the DB password