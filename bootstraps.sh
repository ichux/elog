#!/bin/sh

test -d libraries || mkdir -p libraries

printf "This action OVERWRITES any existing .env file\n\nDo you wish to create them (y/n) as ? "

if [ -z "$1" ]; then
  read answer
else
  answer = $1
fi

create_files(){
cat > .env<< EOF
# PostgreSQL details
PGTZ=Africa/Lagos
POSTGRES_DB=elog
POSTGRES_USER=elog
POSTGRES_PASSWORD=bbaeelog2bdf
POSTGRES_HOST_PORT=9010

# sqlgui app details
SQLGUI_HOST_PORT=9020

# Flask app details
FLASK_ENV=development
FLASK_SKIP_DOTENV=1
FLASK_APP=wsgi.py
FLASK_DEBUG=1
FLASK_RUN_HOST=0.0.0.0

SITE_NAME=elog
SECRET_KEY=bbae57980e2befda27786cd2bd72123f|799427f45298d46f985133720e702ff5
ELAP_STATUS=elog.config.DevelopmentConfig

POSTGRES_HOST=elogpg

SERVER_HOST_PORT=9030
DEV_SERVER_HOST_PORT=9040
SUPERVISOR_HOST_PORT=9050
EOF

printf "\n===\n'.env' has been successfully created\n===\n\n"
}

if [ "$answer" != "${answer#[Yy]}" ] ;then
    create_files
fi