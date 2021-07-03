FORMAT="\nID\t{{.ID}}\nIMAGE\t{{.Image}}\nCOMMAND\t{{.Command}}\nCREATED\t{{.RunningFor}}\nSTATUS\t\
{{.Status}}\nPORTS\t{{.Ports}}\nNAMES\t{{.Names}}\n"

ID_NAME="ID\t{{.ID}}\nNAMES\t{{.Names}}\n"
ELOG_APP = docker exec -it elog_flap


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
	@find . -iname '*.pyc' -delete; find . -iname '.DS_Store' -delete
	@find . -name '__pycache__' -type d -print0 | xargs -0 /bin/rm -rf '{}'


.PHONY: freeze
# help: freeze				- freeze listed Python libraries
freeze:
	@pip freeze | egrep -i "requests|cryptography|wtforms|whoosh|flask-migrate|\
	psycopg2-binary|uwsgitop|flask-login|flask-wtf|blinker|passlib|webtest|\
	python-dotenv|coverage|ua-parser" > requirements.txt


.PHONY: livereload
# help: livereload			- live reload uwsgi
livereload:
	@$(ELOG_APP) touch wsgi.py


.PHONY: bash
# help: bash				- to make bash for the docker environment
bash:
	@$(ELOG_APP) bash


.PHONY: stats
# help: stats				- show live uwsgi statistics
stats:
	@uwsgitop http://127.0.0.1:9030/stats


.PHONY: logs
# help: logs				- to make logs for the docker environment show up
logs:
	@docker-compose logs  --timestamps --follow


.PHONY: build
# help: build				- to make build and then detach from the docker environment
build:
	@docker-compose up --build -d; docker-compose ps  # ; docker-compose logs


.PHONY: stop
# help: stop				- stops docker
stop:
	@docker-compose stop


.PHONY: cls
# help: cls				- to clear the screen
cls:
	@printf "\033c"  # clear the screen


.PHONY: rmi
# help: rmi				- to remove the image with a specified id or id(s. See Makefile for example(s)
rmi:
	@# make rmi id=4152a9608752; make rmi id="1ea5b921a459 07ee12a5eb2a"
	@docker rmi $(id); make cls
	@docker images


.PHONY: tail
# help: tail				- to tail the elog_flap container
tail:
	@docker logs elog_flap --timestamps --follow


.PHONY: dpa
# help: dpa				- to run docker ps -a
dpa:
	@docker-compose ps
	@docker ps -a --format $(FORMAT)

.PHONY: listids
# help: listids				- list all container ids. You can substitute any of them to `make ipdoc id=CONTAINER_ID`
listids:
	@docker ps -a --format $(ID_NAME)


.PHONY: ipdoc
# help: ipdoc				- get the ip of a container. See Makefile for example(s)
ipdoc:
	@# make ipdoc id=4152a9608752
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(id)


.PHONY: routes
# help: routes				- displays the application's routes
routes:
	@$(ELOG_APP) flask routes


.PHONY: shell
# help: shell				- displays the application's shell
shell:
	@$(ELOG_APP) flask shell


.PHONY: dbi
# help: dbi				- to make a development migration init
dbi:
	@$(ELOG_APP) flask dbi


.PHONY: dbm
# help: dbm				- to make a development migration migrate
dbm:
	@$(ELOG_APP) flask dbm


.PHONY: dbr
# help: dbr				- to make a development migration revision
dbr:
	@$(ELOG_APP) flask dbr


.PHONY: dbu_sql
# help: dbu_sql				- to make a development migration upgrade, showing the sql
dbu_sql:
	@$(ELOG_APP) flask dbu-sql


.PHONY: dbu_no_sql
# help: dbu_no_sql			- to make a development migration upgrade, not showing the sql
dbu_no_sql:
	@$(ELOG_APP) flask dbu-no-sql


.PHONY: dd_sql
# help: dd_sql				- to make a development migration downgrade, showing the sql
dd_sql:
	@$(ELOG_APP) flask dd-sql


.PHONY: dd_no_sql
# help: dd_no_sql			- to make a development migration downgrade, not showing the sql
dd_no_sql:
	@$(ELOG_APP) flask dd-no-sql


.PHONY: dbc
# help: dbc				- shows the current migration
dbc:
	@$(ELOG_APP) flask dbc
	@#docker-compose run --rm serve flask dbc


.PHONY: updates
# help: updates				- to make git updates and show branch
updates:
	@git fetch && git merge origin/master; echo; git branch; echo
	@echo "git branch -D "


.PHONY: key
# help: key				- generates random secret key to sign the application. Keep it secure!
key:
	@$(ELOG_APP) python -c \
	'import os, secrets; print(os.urandom(32)); print(secrets.token_hex(16))'


.PHONY: auth
# help: auth				- add a user with specified parameters to the DB. See Makefile for example(s)
auth:
	@# make auth u=ichux p=ichux
	@$(ELOG_APP) flask auth ${u} ${p}


.PHONY: usid
# help: usid				- get the id of the specified user from the DB. See Makefile for example(s)
usid:
	@# make usid u=ichux
	@$(ELOG_APP) flask usid ${u}


.PHONY: access
# help: access				- grants access to a user from an IP address. See Makefile for example(s)
access:
	@# make access u=ichux ip=127.0.0.1
	@$(ELOG_APP) flask access ${u} ${ip}


.PHONY: details
# help: details				- displays the details of a user
details:
	@# make details u=ichux
	@$(ELOG_APP) flask details ${u}


.PHONY: config
# help: config				- displays the docker configuration
config:
	@docker-compose config


.PHONY: ps
# help: ps				- runs the docker ps command
ps:
	@docker-compose ps


.PHONY: lint
# help: lint				- flake8 elog tests
lint:
	@flake8 elog tests


.PHONY: typing
# help: typing				- mypy elog tests
typing:
	@mypy elog tests


.PHONY: test
# help: test                           - run tests
test:
	@docker-compose run --rm serve python -m unittest discover -s tests


.PHONY: cospell
# help: cospell                          - performs codespell on it
cospell:
	@codespell . --skip=*.js,*.txt,*.css,*.wpu \
		--ignore-words-list=eith,gae --skip=./.* --quiet-level=2

.PHONY: ci
# help: ci			 	- these conditions have to pass before you can make a push
ci: lint typing test cospell


.PHONY: coverage
# help: coverage                       - perform test coverage checks
coverage:
	@$(ELOG_APP) coverage erase
	@$(ELOG_APP) coverage run -m unittest discover -s tests -v
	@$(ELOG_APP) coverage html
	@$(ELOG_APP) coverage report
	@# pytest --cov=elog


.PHONY: format
# help: format                         - perform code style format
format:
	@black elog tests


.PHONY: check-format
# help: check-format                   - check code format compliance
check-format:
	@black --check elog tests


.PHONY: sort-imports
# help: sort-imports                   - apply import sort ordering
sort-imports:
	@isort . --profile black


.PHONY: check-sort-imports
# help: check-sort-imports             - checks imports are sorted
check-sort-imports:
	@isort . --check-only --profile black


.PHONY: style
# help: style                          - performs code style format
style: sort-imports format


.PHONY: check-style
# help: check-style                    - check code style compliance
check-style: check-sort-imports check-format


.PHONY: check-types
# help: check-types                    - check type hint annotations
check-types:
	@mypy -p elog tests --ignore-missing-imports


.PHONY: check-lint
# help: check-lint                     - run static analysis checks
check-lint:
	@pylint --rcfile=.pylintrc elog ./tests


.PHONY: check-static-analysis
# help: check-static-analysis          - check code style compliance
check-static-analysis: check-lint check-types


.PHONY: docs
# help: docs                           - generate project documentation
docs: coverage
	@cd docs; rm -rf source/api/elog*.rst source/api/modules.rst build/*
	@cd docs; make html


.PHONY: check-docs
# help: check-docs                     - quick check docs consistency
check-docs:
	@cd docs; make dummy


.PHONY: serve-docs
# help: serve-docs                     - serve project html documentation
serve-docs:
	@cd docs/build; python3 -m http.server --bind 127.0.0.1


.PHONY: dist
# help: dist                           - create a wheel distribution package
dist:
	@python setup.py bdist_wheel


.PHONY: dist-test
# help: dist-test                      - test a wheel distribution package
dist-test: dist
	@cd dist && ../tests/test-dist.bash ./elog-*-py3-none-any.whl


.PHONY: dist-upload
# help: dist-upload                    - upload a wheel distribution package
dist-upload:
	@twine upload dist/elog-*-py3-none-any.whl


.PHONY: pgsql_bash
# help: pgsql_bash                     - PostgreSQL bash
pgsql_bash:
	@echo 'psql "postgresql://postgres:bbaeelog2bdf@elogpg:5432" -c "SHOW data_directory;"'
	@echo 'psql "postgresql://elog:bbaeelog2bdf@elogpg:5432/elog" -c "SHOW data_directory;"'
	@docker exec -it elog_psql bash


.PHONY: producedata
# help: producedata                     - Produce random data to test the API of the application
producedata:
	printf "\033c" && sh apidata.sh


.PHONY: prepare
# help: prepare                     	- Prepare the application for expected standard
prepare: style ci