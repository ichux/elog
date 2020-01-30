#!/bin/bash
set -e

while true; do
   flask dbu-no-sql
   if [[ "$?" == "0" ]]; then
       break
   fi
   echo dbu-no-sql command failed, retrying in 5 secs...
   sleep 5
done

if [ "$1" = 'supervisord' ]; then
    exec /usr/bin/supervisord
fi

exec "$@"