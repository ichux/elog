# Elog

Collect your error logs in any application. This is a Flask app and this *README.md* is still being updated.

# Before you begin
1. *source bootstraps.sh* then alter to taste, if need be.
2. `make download` and `make install` to download & install the necessary libraries.
3. If you encounter errors during the build of uwsgi, blinker, uwsgitop, pyperclip and wrapt, just overlook it.
4. Install `pre-commit` on Mac with `brew install pre-commit` or on Linux with `sudo snap install pre-commit --classic`
4. Run `pre-commit install` for you to be able to make use of *.pre-commit-config.yaml*

# Note
1. Ports are quoted here, e.g. 9030. Please note that if you have changed such quoted ports in your `.env` file,
remember to change it to taste where appropriate.

# How to use
1. Type `make` and choose any command that shows afterwards
2. To reload the application run by nginx: type `make livereload`

# To create a user for the application
1. Type `make auth u=username p=password`
2. Visit http://127.0.0.1:9030/
3. Enter the details you created in Step 1 above
4. If you will be using the app through its API then do the following Steps
5. Type `make access u=username ip=IP-ADDRESS` to assign an IP the `username` you created in Step 1
6. Type `make details u=username` to get the details of a `username`

Note: Step 5 will produce a Unique ID that will be added to headers of each request for the API to honour such!

# To view app metrics or monitor it
1. Activate your virtual environment (not inside the container)
2. Type `make stats` or visit http://127.0.0.1:9030/stats
3. [inet_http_server](customize/supervisord.conf) details
4. Visit http://127.0.0.1:9050/ and use the credentials from Step 4. to access it

# To run the application for development
1. type `make bash` to enter the container
2. run `flask run --host 0.0.0.0`

# Bootstrap the application
1. `make build`
2. `make routes` displays all the routes so that you can know which one to work with
3. `docker-compose ps` helps you see the running apps and the ports they are serving on

# DB manager
[adminer](https://www.adminer.org/) is used to interface the DB of this application.
[Here](customize/adminer-elog-settings.png) is a sample configuration


# Important
1. Some commands like `make usid`, `make auth` have commented lines in the [Makefile](Makefile) on how to use them.
2. run `pre-commit install` for you to be able to make use of *.pre-commit-config.yaml*

# PR
If you find anything that needs to be taken care of, please submit a PR.
