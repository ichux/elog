#!/bin/sh
set -e

LOCATION=/var/www/migrations

# prime the DB to be sure that it is up and running
# python3.7 prime_db.py
printf "import os\nimport time\n\nimport psycopg2\n\n\ndef primes():\n    \
def connect():\n        connection = None\n        \
host, database = os.getenv('POSTGRES_HOST'), os.getenv('POSTGRES_DB')\n        \
user, password = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')\n\n        \
try:\n            \
connection = psycopg2.connect(\n                \
**{\n                    \
  'host': host,\n                    \
  'database': database,\n                    \
  'user': user,\n                    \
  'password': password,\n                \
}\n            )\n            return True\n       \
 except (Exception,):\n            \
 return False\n        finally:\n            if connection:\n                \
 connection.close()\n\n    while True:\n        if connect():\n            \
 break\n\n        print('sleeping for 3s..')\n        time.sleep(3)\n\n\nprimes()" \
 | /usr/bin/env python3 && echo "DB is Up"

# initialise the migration if it hasn't been done
# if [ ! -d "$LOCATION" ]; then
#   flask dbi
# fi

# # run the migration if there is one in existence
# if [ -d "$LOCATION" ]; then
#   flask dbm;

#   if flask dbu-no-sql; then
#     echo database migrations have been run!
#   fi
# fi

if [ "$1" = 'supervisord' ]; then
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi

exec "$@"