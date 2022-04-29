# Elog

Collect your error logs in any application. This is a Flask app and this is still being updated.

This guide is intended for development setup.

# Before you begin
1. Clone the repo
```bash
git clone https://github.com/ichux/elog.git
cd elog
```
2. *source bootstraps.sh* then alter to taste, if need be.
3. Create a virtual env and install dependencies
```bash
python3 -m venv .venv
. .venv/bin/activate # For linux, see bin/ for your system script 
python -m pip install -r requirements.txt -r requirements-dev.txt
```
3. If you encounter errors during the build of uwsgi, blinker, uwsgitop, pyperclip and wrapt, just overlook it.
4. Run `pre-commit install` for you to be able to make use of *.pre-commit-config.yaml*

# Note
1. Ports are quoted here, e.g. 9030. Please note that if you have changed such quoted ports in your `.env` file,
remember to change it to taste where appropriate.

# Start the app
1. Run the database migrations
```bash
python -m flask db migrate 
python -m flask db upgrade 
```
2. [Create a user](#to-create-a-user-for-the-application)
3. Then run the development server with 
```bash
python -m flask run # --port or --host to customize
```
Go to `localhost:5000`(default port for Flask) to see you app live.

# To create a user for the application
1. Type `flask auth {username} {password}`. Do note that you have to replace anything within brackets with your values.

# Testing the application
1. To run unit tests, `pytest tests/unit`
2. To can e2e tests, `pytest test/e2e`. make sure to have Chrome browser installed.
Or See [SeleniumBase docs](https://seleniumbase.io/help_docs/) to adapt to your environment (e.g using Firefox, --browser=firefox).

# An overview of the code organization
The main part lives in the `elog` subdirectory. Other folders and files are either config files or needed for the app to run, like `logsdir` for storing the logs. Here is how the `elog` is organized.
```bash
elog
├── advsearch.py
├── commands.py
├── config.py
├── controllers/ # Contains Flask app and Blueprints
├── errorhandlers.py
├── errortraps.py
├── forms/
├── helpers.py
├── __init__.py
├── models/
├── static/ # The minified version of static assets
├── static-generator/ # Contain code to generate static assets. See its README.
└── templates/ # Jinja templates for server-side rendering

6 directories, 7 files
```