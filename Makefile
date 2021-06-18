FORMAT="\nID\t{{.ID}}\nIMAGE\t{{.Image}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.RunningFor}}\nSTATUS\t\
{{.Status}}\nPORTS\t{{.Ports}}\nNAMES\t{{.Names}}\n"

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: elog Makefile help
# help:

.PHONY: help
# help: help				- Please use "make <target>" where <target> is one of
help:
	@grep "^# help\:" Makefile | sed 's/\# help\: //' | sed 's/\# help\://'



.PHONY: clean
# help: clean 				- to make the work directories clean of unwanted files
clean:
	find . -iname '*.pyc' -delete; find . -iname '.DS_Store' -delete
	find . -name '__pycache__' -type d -print0 | xargs -0 /bin/rm -rf '{}'


.PHONY: freeze
# help: freeze				- freeze listed Python libraries
freeze:
	@pip freeze | egrep -i "requests|cryptography|wtforms|whoosh|flask-migrate" > requirements.txt


.PHONY: bash
# help: bash				- to make bash for the docker environment
bash: clean
	docker exec -it elog_flap bash


.PHONY: logs
# help: logs				- to make logs for the docker environment show up
logs:
	docker-compose logs  --timestamps --follow


.PHONY: bde
# help: bde				- to make build and then detach from the docker environment
bde: clean
	docker-compose up --build -d; docker-compose logs; docker-compose ps


.PHONY: up
# help: up				- powers up docker
up:
	docker-compose up --build -d


.PHONY: stop
# help: stop				- stops docker
stop:
	docker-compose stop


.PHONY: cls
# help: cls				- to clear the screen
cls:
	printf "\033c"  # clear the screen


.PHONY: down
# help: down				- to make the docker environment go down and clean itself up
down:
	docker-compose down
	docker images; echo
	@echo 'make rmi id="'


.PHONY: rmi
# help: rmi				- to remove the image with a specified id or id(s. See Makefile for example(s)
rmi:
    # make rmi id=4152a9608752; make rmi id="1ea5b921a459 07ee12a5eb2a"
	docker rmi $(id); make cls
	docker images


.PHONY: tail
# help: tail				- to tail the elog_flap container
tail:
	docker logs elog_flap --timestamps --follow


.PHONY: dpa
# help: dpa				- to run docker ps -a
dpa:
	docker-compose ps
	docker ps -a --format $(FORMAT)


.PHONY: ipdoc
# help: ipdoc				- get the ip of a container. See Makefile for example(s)
ipdoc:
    # make ipdoc id=4152a9608752
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(id)


.PHONY: psdoc
# help: psdoc				- to run docker-compose ps
psdoc:
	docker-compose ps


.PHONY: routes
# help: routes				- displays the application's routes
routes:
	docker-compose run --rm serve flask routes


.PHONY: shell
# help: shell				- displays the application's shell
shell:
	docker-compose run --rm serve flask shell


.PHONY: dbi
# help: dbi				- to make a development migration init
dbi:
	docker-compose run --rm serve flask dbi


.PHONY: dbm
# help: dbm				- to make a development migration migrate
dbm:
	docker-compose run --rm serve flask dbm


.PHONY: dbr
# help: dbr				- to make a development migration revision
dbr:
	docker-compose run --rm serve flask dbr


.PHONY: dbu_sql
# help: dbu_sql				- to make a development migration upgrade, showing the sql
dbu_sql:
	docker-compose run --rm serve flask dbu-sql


.PHONY: dbu_no_sql
# help: dbu_no_sql			- to make a development migration upgrade, not showing the sql
dbu_no_sql:
	docker-compose run --rm serve flask dbu-no-sql


.PHONY: dd_sql
# help: dd_sql				- to make a development migration downgrade, showing the sql
dd_sql:
	docker-compose run --rm serve flask dd-sql


.PHONY: dd_no_sql
# help: dd_no_sql			- to make a development migration downgrade, not showing the sql
dd_no_sql:
	docker-compose run --rm serve flask dd-no-sql


.PHONY: dbc
# help: dbc				- shows the current migration
dbc:
	docker-compose run --rm serve flask dbc


.PHONY: updates
# help: updates				- to make git updates and show branch
updates:
	git checkout master && git fetch && git merge origin/master; echo
	git branch; echo
	@echo "git branch -D "


.PHONY: key
# help: key				- generates random secret key to sign the application. Keep it secure!
key:
	docker-compose run --rm serve python -c 'import os; print(os.urandom(32))'


.PHONY: auth
# help: auth				- add a user with specified parameters to the DB. See Makefile for example(s)
auth:
	# make auth u=ichux p=ichux
	docker-compose run --rm serve flask auth ${u} ${p}


.PHONY: usid
# help: usid				- get the id of the specified user from the DB. See Makefile for example(s)
usid:
	# make usid u=ichux
	docker-compose run --rm serve flask usid ${u}


.PHONY: access
# help: access				- grants access to a user. See Makefile for example(s)
access:
	# make access u=ichux ip=127.0.0.1
	docker-compose run --rm serve flask access ${u} ${ip} ${id}


.PHONY: details
# help: details				- displays the details of a user
details:
	# make details u=ichux
	docker-compose run --rm serve flask details ${u}


.PHONY: config
# help: config				- displays the docker configuration
config:
	docker-compose config


.PHONY: ps
# help: ps				- runs the docker ps command
ps:
	docker-compose ps


.PHONY: run
# help: run				- starts the application in debug mode with the flask cli
run:
	flask run --host 0.0.0.0


.PHONY: viup
# help: viup				- bring the supervisorctl up
viup:
	supervisorctl start all


.PHONY: vidown
# help: vidown				- take the supervisorctl down
vidown:
	supervisorctl stop all


.PHONY: vistat
# help: vistat				- tells you the status of supervisor
vistat:
	supervisorctl status


.PHONY: migrate
# help: migrate				- to make migrations reflect in the DB
migrate:
