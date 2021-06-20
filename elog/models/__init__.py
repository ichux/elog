from collections import OrderedDict
from datetime import datetime
from json import dumps, loads
from pprint import pprint

from psycopg2.extensions import adapt as sqlescape  # type: ignore
from sqlalchemy.sql import compiler  # type: ignore

from elog import db, elap  # type: ignore

# CONSTANTS
NAME = 400
DESCRIPTION = 400

# FOR THE DB
CASCADE = elap.config.get("CASCADE")  # type: ignore
LAZY = elap.config.get("LAZY")  # type: ignore


def documentation():
    """
    The models in this package would have to scale and as such,
    there would always be 2 model file:
    found in readonly and readwrite packages

    ***readonly is to be used only for read requests
    ***readwrite is to be used only for write requests.

    So, you should import it like this:
    from modelate.models.writeonly import user_wo
    And call it like this:
    user_wo.query.filter_by(username=username).first()

    OR

    from modelate.models.writeonly import *
    With the "import *", all the packages stated in the "__all__" variable
    would be visible in the scope of the file

    This method is to make it apparent when reading and writing to the database.

    And, most importantly, readonly and readwrite packages must always contain
    the same thing, only the
     __bind_key__ = 'readonly' should differ in the files with 'class'"""


# noinspection PyUnresolvedReferences
class HouseKeeping(object):
    def add(self):
        db.session.add(self)  # type: ignore
        db.session.commit()  # type: ignore

    def named(self):
        return self.__table__.name  # .lower()

    def display(self):
        pprint(loads(json_data(self.__table__.name, self.id)))

    def as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():  # OR self.__table__.columns.keys()
            result[key] = getattr(self, key)
        return result

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def columns(cls):
        return cls.__table__.columns.keys()

    @classmethod
    def relationships(cls):
        """
        Returns a relationship and indicates if it's a list (True) or not
        :return: list
        """
        return [
            [_, "is_list: {}".format(cls.__mapper__.relationships[_].uselist)]
            for _ in cls.__mapper__.relationships.keys()
        ]

    @classmethod
    def get_field_and_relationships(cls):
        return dict(
            table_name=cls.__table__.name,
            columns=cls.columns(),
            relationships=cls.relationships(),
        )


class Base(db.Model, HouseKeeping):  # type: ignore
    """Base model that other specific models inherit from"""

    __abstract__ = True

    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # type: ignore
    modified_on = db.Column(  # type: ignore
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow  # type: ignore
    )

    # BigInteger range: -9223372036854775808 to 9223372036854775807
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # type: ignore
    enabled = db.Column(db.Boolean, nullable=False, default=True)  # type: ignore


def remove_json_unwanted(*args):
    result = args[0]
    for each in args[1:]:
        result.pop(each, None)
    return result


def date_handler(value):
    """
    Return a string type of Python datetime format
    :param value: datetime of Python
    :return: string
    """
    return value.isoformat() if hasattr(value, "isoformat") else value


# noinspection PyProtectedMember
def get_class_by_tablename(tablename):
    for c in db.Model._decl_class_registry.values():  # type: ignore
        if hasattr(c, "__tablename__") and c.__tablename__ == tablename:
            return c


# noinspection PyProtectedMember
def json_data(tablename, _id):
    """
    Returns the json representation of a table. It converts any datetime object to
    a string representation of the time
    :param tablename: The name of the table: User.query.get(1).named()
    :param _id: the id of the table to query
    :return: json format
    """
    return dumps(
        get_class_by_tablename(tablename).query.get(_id).as_dict(), default=date_handler
    )


def cleanup():
    db.session.rollback()
    db.session.commit()
    print("DB in a clean state")


def latest(_class):
    db.engine.echo = False
    try:
        print("\n")
        return _class.query.order_by(_class.id.desc()).first().display()
    except (Exception,):
        cleanup()
        print("\nNo data found")


# noinspection PyProtectedMember
def show_all():
    classes, models, table_names = [], [], []
    for clazz in db.Model._decl_class_registry.values():
        if hasattr(clazz, "__tablename__"):
            table_names.append(clazz.__tablename__)
            classes.append(clazz)

    for table in db.metadata.tables.items():
        if table[0] in table_names:
            models.append(classes[table_names.index(table[0])])

    return classes, models, table_names


# noinspection PyProtectedMember
def show_classes():
    classes = []
    for clazz in db.Model._decl_class_registry.values():
        if hasattr(clazz, "__tablename__"):
            classes.append(clazz)
    return classes  # classes[0].query.get(1)


# noinspection PyProtectedMember
def get_class(table_name):
    for clazz in db.Model._decl_class_registry.values():
        if hasattr(clazz, "__tablename__"):
            if clazz.__tablename__ == table_name:
                return clazz
    return None


# noinspection PyArgumentList
def compile_query(query):
    dialect = query.session.bind.dialect

    comp = compiler.SQLCompiler(dialect, query.statement)
    comp.compile()

    enc = dialect.encoding
    params = {}
    for k, v in comp.params.iteritems():
        if isinstance(v, str):
            v = v.encode(enc)
        params[k] = sqlescape(v)

    return (comp.string.encode(enc) % params).decode(enc)
