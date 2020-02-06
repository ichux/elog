# Elog

Collect your error logs in any application. This is a Flask app and this *README.md* is still being updated.

# How to use
Care has been taken to ensure that the Makefile commands are all documented. But then, if there is anyone that is
missing, do let me know by submitting a PR

> 1. Type `make` and choose any command that shows afterwards
> 2. To reload the application run by nginx

>   a. `make bash` to enter the container

>   b. then type `touch wsgi.py`
> 3. If you need auto-reload during development, then type `make run`

# Bootstrap the application
1. `make bde` *OR* `make up`
2. `make routes` displays all the routes so that you can know which one to work with
3. `docker-compose ps` helps you see the running apps and the ports they are serving on

# DB manager
[adminer](https://www.adminer.org/) is used to interface the DB of this application.
[Here](customize/adminer-elog-settings.png) is a sample configuration

# Determine the IP address of the localhost
This is necessary if you want to access this application from another docker instance. It is just a hack to ensure that
things work fine across all OS. There is the option of adding `HOST_IP: 'host.docker.internal'` to the 
docker-compose.yml file but it does not work in a production environment outside of Docker Desktop for Mac!
1. `cd edock`
2. Follow the `STEP 1` stated [here](edock/steps.txt)
3. Follow `CLEAN UP` stated [here](edock/steps.txt) to clean up after you are done

# Important
Some commands like `make usid`, `make auth` have commented lines in the [Makefile](Makefile) on how to use them.