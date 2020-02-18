#!/bin/sh
set -e

LOCATION=/var/www/migrations

# prime the DB to be sure that it is up and running
python3.7 prime_db.py

# initialise the migration if it hasn't been done
if [ ! -d "$LOCATION" ]; then
  flask dbi
fi

# run the migration if there is one in existence
if [ -d "$LOCATION" ]; then
  flask dbm;

  if flask dbu-no-sql; then
    echo database migrations have been run!
  fi
fi

if [ "$1" = 'supervisord' ]; then
    exec /usr/bin/supervisord
fi

exec "$@"