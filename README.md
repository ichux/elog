# Elog

Collect your error logs in any application. This is a Flask app and this *README.md* is still being updated.

# How to use
Care has been taken to ensure that the Makefile commands are all documented. But then, if there is anyone that is
missing, do let me know by submitting a PR

Important: *cp .prime.env .env*

> 1. Type `make` and choose any command that shows afterwards
> 2. To reload the application run by nginx

>   a. `make bash` to enter the container

>   b. then type `touch wsgi.py`
> 3. If you need auto-reload during development, then type `make run`

# To run the application for development
1. type `make bash` to enter the container
2. run `flask run --host 0.0.0.0`

# Bootstrap the application
1. `make bde` *OR* `make up`
2. `make routes` displays all the routes so that you can know which one to work with
3. `docker-compose ps` helps you see the running apps and the ports they are serving on

# DB manager
[adminer](https://www.adminer.org/) is used to interface the DB of this application.
[Here](customize/adminer-elog-settings.png) is a sample configuration


# Important
1. Some commands like `make usid`, `make auth` have commented lines in the [Makefile](Makefile) on how to use them.
2. run `pre-commit install` for you to be able to make use of *.pre-commit-config.yaml*
