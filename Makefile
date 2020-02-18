FORMAT="\nID\t{{.ID}}\nIMAGE\t{{.Image}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.RunningFor}}\nSTATUS\t\
{{.Status}}\nPORTS\t{{.Ports}}\nNAMES\t{{.Names}}\n"

help:
	make cls
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  clean           to make the work directories clean of unwanted files"
	@echo "  bash            to make bash for the docker environment"
	@echo "  logs            to make logs for the docker environment show up"
	@echo "  bde             to make build and then detach from the docker environment"
	@echo "  up              powers up docker"
	@echo "  stop            stops docker"
	@echo "  cls             to clear the screen"
	@echo "  down            to make the docker environment go down and clean itself up"
	@echo "  rmi             to remove the image with a specified id or id(s)"
	@echo "  tail            to tail the elog_flap container"
	@echo "  dpa             to run docker ps -a"
	@echo "  ipdoc           get the ip of a container"
	@echo "  psdoc           to run docker-compose ps"
	@echo "  routes          displays the application's routes"
	@echo "  shell           displays the application's shell"

	@echo "  dbi             to make a development migration init"
	@echo "  dbm             to make a development migration migrate"
	@echo "  dbr             to make a development migration revision"
	@echo "  dbu_sql         to make a development migration upgrade, showing the sql"
	@echo "  dbu_no_sql      to make a development migration upgrade, not showing the sql"
	@echo "  dd_sql          to make a development migration downgrade, showing the sql"
	@echo "  dd_no_sql       to make a development migration downgrade, not showing the sql"
	@echo "  dbc             shows the current migration"

	@echo "  updates        to make git updates and show branch"
	@echo "  key            generates random secret key to sign the application. Keep it secure!"
	@echo "  auth           add a user with specified parameters to the DB"
	@echo "  usid           get the id of the specified user from the DB"
	@echo "  access         grants access to a user"
	@echo "  details        displays the details of a user"
	@echo "  config         displays the docker configuration"
	@echo "  ps             runs the docker ps command"
	@echo "  run            starts the application in debug mode with the flask cli"
	@echo "  viup           bring the supervisorctl up"
	@echo "  vidown         take the supervisorctl down"
	@echo "  vistat         tells you the status of supervisor"
	@echo "  migrate         to make migrations reflect in the DB"


clean:
	find . -iname '*.pyc' -delete; find . -iname '.DS_Store' -delete
	find . -name '__pycache__' -type d -print0 | xargs -0 /bin/rm -rf '{}'

bash: clean
	docker exec -it elog_flap bash

logs:
	docker-compose logs  --timestamps --follow

bde: clean
	docker-compose up --build -d; docker-compose logs; docker-compose ps

up:
	docker-compose up --build -d

stop:
	docker-compose stop

cls:
	printf "\033c"  # clear the screen

down:
	docker-compose down
	docker images; echo
	@echo 'make rmi id="'

rmi:
    # make rmi id=4152a9608752; make rmi id="1ea5b921a459 07ee12a5eb2a"
	docker rmi $(id); make cls
	docker images

tail:
	docker logs elog_flap --timestamps --follow

dpa:
	docker-compose ps
	docker ps -a --format $(FORMAT)

ipdoc:
    # make ipdoc id=4152a9608752
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(id)

psdoc:
	docker-compose ps

routes:
	docker-compose run --rm serve flask routes

shell:
	docker-compose run --rm serve flask shell

dbi:
	docker-compose run --rm serve flask dbi

dbm:
	docker-compose run --rm serve flask dbm

dbr:
	docker-compose run --rm serve flask dbr

dbu_sql:
	docker-compose run --rm serve flask dbu-sql

dbu_no_sql:
	docker-compose run --rm serve flask dbu-no-sql

dd_sql:
	docker-compose run --rm serve flask dd-sql

dd_no_sql:
	docker-compose run --rm serve flask dd-no-sql

dbc:
	docker-compose run --rm serve flask dbc

updates:
	git checkout master && git fetch && git merge origin/master; echo
	git branch; echo
	@echo "git branch -D "

key:
	docker-compose run --rm serve python -c 'import os; print(os.urandom(32))'

auth:
	# make auth u=ichux p=ichux
	docker-compose run --rm serve flask auth ${u} ${p}

usid:
	# make usid u=ichux
	docker-compose run --rm serve flask usid ${u}

access:
	# make access u=ichux ip=127.0.0.1
	docker-compose run --rm serve flask access ${u} ${ip} ${id}

details:
	# make details u=ichux
	docker-compose run --rm serve flask details ${u}

config:
	docker-compose config

ps:
	docker-compose ps

run:
	flask run --host 0.0.0.0

viup:
	supervisorctl start all

vidown:
	supervisorctl stop all

vistat:
	supervisorctl status

migrate:
	make cls
	sh entrypoint.sh