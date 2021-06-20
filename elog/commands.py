import os
import secrets
import time
from datetime import datetime

import click
from flask_migrate import (  # type: ignore
    current,
    downgrade,
    init,
    migrate,
    revision,
    upgrade,
)

from elog import db, elap
from elog.models.profile import User, UserAccess


class Usable(object):
    def __init__(self):
        self.time = datetime.utcfromtimestamp(time.time())
        self.directory = os.path.join(os.getcwd(), "migrations", "versions")

    def message(self):
        return self.time.strftime("%Y_%m_%d")

    def revision_id(self):
        path, dirs, files = next(os.walk(self.directory))
        return str(len([file_ for file_ in files if file_.endswith(".py")]) + 1).zfill(
            6
        )


@elap.cli.command("dbi")
def dbi():
    """
    Calls the init()
    :return: None
    """
    init()


@elap.cli.command("dbm")
def dbm():
    """
    Calls the migrate()
    :return: None
    """
    usable = Usable()
    migrate(message=usable.message(), rev_id=usable.revision_id())


@elap.cli.command("dbr")
def dbr():
    """
    Calls the revision()
    :return: None
    """
    usable = Usable()
    revision(message=usable.message(), rev_id=usable.revision_id())


@elap.cli.command("dbu-sql")
def dbu_sql():
    """
    Generate SQL statements but you will personally have to `run` it on your DB
    :return: None
    """
    upgrade(sql=True)


@elap.cli.command("dbc")
def db_current():
    """
    Calls the current()
    :return: None
    """
    current()


@elap.cli.command("dbu-no-sql")
def dbu_no_sql():
    """
    Bring the DB up to date with your data models.
    Calls the migrate()
    :return: None
    """
    upgrade()


@elap.cli.command("dd-sql")
def downgrade_sql():
    """
    Generate SQL statements but you will personally have to `run` it on your DB
    :return: None
    """
    downgrade(sql=True)


@elap.cli.command("dd-no-sql")
def downgrade_no_sql():
    """
    Bring the DB up to date with your data models.
    Calls the downgrade()
    :return: None
    """
    downgrade()


@elap.cli.command("auth")
@click.argument("username")
@click.argument("password")
def add_auth(username, password):
    """
    It adds a User to the DB
    :return: None
    """

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    print(f"\n`{username}` with id={user.id} has been added to the DB\n")


@elap.cli.command("usid")
@click.argument("username")
def user_id(username):
    """
    It gets a user id from the DB
    :return: None
    """

    user = User.query.filter_by(username=username).first()
    if user:
        print(f"\n{username} with id={user.id} was found\n")
    else:
        print(f"\nThe username `{username}` was not found!\n")


@elap.cli.command("access")
@click.argument("username")
@click.argument("ip_address")
def add_access(username, ip_address):
    """
    It adds an access for a User to the DB
    :return: None
    """

    user = User.query.filter_by(username=username).first()
    if user:
        user_access = UserAccess(users_id=user.id, ip_address=ip_address)
        user_access.external_app_id = secrets.randbits(32)

        db.session.add(user_access)
        db.session.commit()
        print(f"\n`external_app_id = {user_access.external_app_id}`\n")
    else:
        print(f"\nThe username `{username}` was not found!\n")


@elap.cli.command("details")
@click.argument("username")
def details(username):
    """
    It adds a User to the DB
    :return: None
    """

    user = User.query.filter_by(username=username).first()
    if user:
        print("\n")
        for _ in user.known_access:
            _.display()
            print("\n")
    else:
        print(f"\nThe username `{username}` was not found!\n")
