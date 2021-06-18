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


.PHONY: lint
# help: lint				- flake8 elog tests
lint:
	flake8 elog tests


.PHONY: typing
# help: typing				- mypy elog tests
typing:
	mypy elog tests


.PHONY: coverage
# help: coverage			- runs pytest --cov=elog
coverage:
	pytest --cov=elog


.PHONY: ci
# help: ci				- for a sort passing of some conditions before it can be pushed
ci: lint typing test


# help: test                           - run tests
.PHONY: test
test:
	python -m unittest discover -s tests  # pytest


# help: test-verbose                   - run tests [verbosely]
.PHONY: test-verbose
test-verbose:
	python -m unittest discover -s tests -v


# help: coverage                       - perform test coverage checks
.PHONY: coverage
coverage:
	@coverage erase
	coverage run -m unittest discover -s tests -v
	@coverage html
	@coverage report


# help: format                         - perform code style format
.PHONY: format
format:
	black elog tests


# help: check-format                   - check code format compliance
.PHONY: check-format
check-format:
	black --check elog tests


# help: sort-imports                   - apply import sort ordering
.PHONY: sort-imports
sort-imports:
	isort . --profile black


# help: check-sort-imports             - check imports are sorted
.PHONY: check-sort-imports
check-sort-imports:
	isort . --check-only --profile black


# help: style                          - perform code style format
.PHONY: style
style: sort-imports format


# help: check-style                    - check code style compliance
.PHONY: check-style
check-style: check-sort-imports check-format


# help: check-types                    - check type hint annotations
.PHONY: check-types
check-types:
	mypy -p elog --ignore-missing-imports


# help: check-lint                     - run static analysis checks
.PHONY: check-lint
check-lint:
	@pylint --rcfile=.pylintrc elog ./tests


# help: check-static-analysis          - check code style compliance
.PHONY: check-static-analysis
check-static-analysis: check-lint check-types


# help: docs                           - generate project documentation
.PHONY: docs
docs: coverage
	@cd docs; rm -rf source/api/elog*.rst source/api/modules.rst build/*
	@cd docs; make html


# help: check-docs                     - quick check docs consistency
.PHONY: check-docs
check-docs:
	@cd docs; make dummy


# help: serve-docs                     - serve project html documentation
.PHONY: serve-docs
serve-docs:
	cd docs/build; python -m http.server --bind 127.0.0.1


# help: dist                           - create a wheel distribution package
.PHONY: dist
dist:
	python setup.py bdist_wheel


# help: dist-test                      - test a wheel distribution package
.PHONY: dist-test
dist-test: dist
	@cd dist && ../tests/test-dist.bash ./elog-*-py3-none-any.whl


# help: dist-upload                    - upload a wheel distribution package
.PHONY: dist-upload
dist-upload:
	twine upload dist/elog-*-py3-none-any.whl


# help: gm                    - runs "git fetch && git merge origin/master"
.PHONY: gm
gm:
	git fetch && git merge origin/master
