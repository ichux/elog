import pkg_resources

libs = """alembic
blinker
certifi
cffi
chardet
Click
coverage
cryptography
Flask
Flask-Login
Flask-Migrate
Flask-SQLAlchemy
Flask-WTF
idna
itsdangerous
Jinja2
Mako
MarkupSafe
passlib
psycopg2-binary
pycparser
pyOpenSSL
python-dateutil
python-dotenv
python-editor
requests
requests-toolbelt
six
SQLAlchemy
ua-parser
uwsgitop
WebTest
Werkzeug
Whoosh
WTForms
"""

collate = []

for installed_version in [
    str(iv).replace(" ", "==") for iv in pkg_resources.working_set
]:
    for file_version in libs.split():
        if f"{file_version}==" in installed_version:
            collate.append(installed_version)
            break

print("\n".join(sorted(collate)))
