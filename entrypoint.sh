#!/bin/sh
set -e

# prime the DB to be sure that it is up and running
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
 | /usr/bin/env python3 > /dev/null 2>&1

# a hack to run migrations
printf "import os; os.system('flask dbi > /dev/null 2>&1; \
flask dbm > /dev/null 2>&1; flask dbu-no-sql > /dev/null 2>&1')" \
| /usr/bin/env python3


if [ "$1" = 'supervisord' ]; then
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi

exec "$@"
