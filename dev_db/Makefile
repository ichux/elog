help:
	make cls
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  cls             to clear the screen"
	@echo "  up              powers up docker"
	@echo "  stop            stops docker"
	@echo "  down            to make the docker environment go down and clean itself up"
	@echo "  tail            to tail the elog_nexus_db container"
	@echo "  dpa             to run docker ps -a"
	@echo "  config         displays the docker configuration"

cls:
	printf "\033c"  # clear the screen

up:
	docker-compose up --build -d

stop:
	docker-compose stop

down:
	docker-compose down

tail:
	docker logs elog_nexus_db --timestamps --follow

dpa:
	docker-compose ps

config:
	docker-compose config