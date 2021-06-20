import os

from flask import Flask, current_app
from flask.signals import Namespace
from flask_login import LoginManager  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_wtf.csrf import CSRFProtect  # type: ignore
from whoosh import index, qparser, sorting  # type: ignore
from whoosh.qparser.dateparse import DateParserPlugin  # type: ignore
from whoosh.writing import AsyncWriter  # type: ignore

from elog import advsearch
from elog.helpers import metadata

elap = application = Flask(__name__)
elap.config.from_object(os.getenv("ELAP_STATUS"))

csrf = CSRFProtect(elap)
db = SQLAlchemy(elap, metadata=metadata)
Migrate(elap, db)

# manage login
login_manager = LoginManager()
login_manager.init_app(elap)
login_manager.login_view = "auth.login"


def ix_searcher(locate):
    ix = current_app.config.get(locate)
    if not ix.up_to_date():
        ix.refresh()
    return ix


def remove_by_id(doc_id, locate="ELIX"):
    writes = AsyncWriter(ix_searcher(locate))
    writes.delete_by_term("id", doc_id)
    writes.commit()


# noinspection PyUnusedLocal,PyTypeChecker
def data_tables_display(qs, pagenum, pagelen, locate):
    """fetch archived error messages for display
    :param qs: the query string as sent from the web e.g. 'Rain* OR subdomain:asch OR address:osun'
    :type qs: string type
    :param locate: indicates the index to search
    :type locate: index of Whoosh type
    :param pagelen: the total amount we want to display per page e.g on page 1 display 20 items
    :type pagelen: an integer value
    :param pagenum: the page number e.g. page 1, page 2
    :type pagenum: an integer value
    """
    with ix_searcher(locate).searcher() as searcher:
        # print 'details' in searcher.schema.names()  # checks for the presence of a field in the schema
        # fieldboosts = {"code": 2.0, "id": 0.5}
        # 500^2 or code:500^2 are same as hard coding the fieldboosts added to the "MultifieldParser"
        query = qparser.MultifieldParser(
            ["errormsg", "errortype", "id", "ip", "code", "date", "when"],
            searcher.schema,
        )
        query.add_plugins(
            (
                DateParserPlugin(),
                qparser.GtLtPlugin(),
                qparser.SequencePlugin("!(~(?P<slop>[1-9][0-9]*))?"),
            )
        )
        # details(query)

        # pagelen = min(pagelen, current_app.config['MAX_WHOOSH_SEARCH_RESULTS'])

        try:
            # this has to be done because the jQuery datatables might throw in an int which
            # whoosh does not need. It needs all its values to be of <type 'unicode'>
            getattr(qs, "decode")
        except AttributeError:
            qs = str(qs)

        try:

            # this is a hack. Datatable sends in the total number of items present on
            # each page but not the next page number. Whoosh expects the next page number
            if pagenum > 1:
                # total_length = len(searcher.search(query.parse('ip:*')))  # this is a hack
                pagenum, _ = divmod(pagenum, pagelen)
                pagenum += 1

            mf = sorting.MultiFacet()
            # mf.add_field("code", reverse=True)
            mf.add_field(
                "date", reverse=True
            )  # sorts the result in descending order by date

            results = searcher.search_page(
                query.parse(qs), pagenum, pagelen, sortedby=mf, terms=True
            )
        except (Exception,):
            results = {}

        output = []
        if len(results) > 0:
            """
            print("Last page: %s" % results.is_last_page())
            print("Page %d of %d" % (results.pagenum, results.pagecount))
            later = results.offset + results.pagelen + 1
            print("Showing results %d-%d of %d" % (results.offset + 1, later, len(results)))
            """
            # details(dir(results))

            for hit in results:
                # print("hit.more_like_this: {}".format(hit.more_like_this))
                loops = []
                for key, value in hit.iteritems():
                    loops.append((key, value))
                output.append(dict(loops))

                # what terms matched in each hit
                # print(hit.matched_terms())
                #
                # keeps = {}
                # for key, value in hit.iteritems():
                #     """
                #     if key == 'details':
                #         # this is done to make sure that it display properly on the web page
                #         pd = current_app.config['PARENT_DIR']
                #         keeps[ARRANGED_AS.get(key)] = value.replace('\n', '<br>').replace(pd, 'ROOT')
                #     else:
                #         keeps[ARRANGED_AS.get(key)] = value
                #     """
                #     print(key, value)
                # output.append(keeps)
                #
        pushout = []
        for step in output:
            errortraceback = step.get("errortraceback")
            if errortraceback:
                step["errortraceback"] = errortraceback.replace("\n", "<br>")
                pushout.append(step)

        return {
            "recordsTotal": searcher.reader().doc_count(),
            "recordsFiltered": len(results),
            "data": pushout,
        }


fortress = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../logsdir")
)

# create FORTRESS directory
if not os.path.exists(fortress):
    try:
        os.mkdir(fortress)
    except (Exception,):
        pass

if not index.exists_in(fortress, indexname="elogindex"):
    elap.config.update(
        ELIX=index.create_in(fortress, advsearch.ErrorLogsSchema, indexname="elogindex")
    )
else:
    elap.config.update(ELIX=index.open_dir(fortress, indexname="elogindex"))


def write_async(kwargs, where):
    """
    Function to use the AsyncWriter to avoid cluttering.

    :param kwargs: <type 'dict'>
    :param where: which place to load the index from

    """
    # writer = BufferedWriter(ix_searcher('ELIX'), period=0.25, limit=10, writerargs={'procs': 4, 'limitmb': 128})
    # writer = AsyncWriter(ix_searcher('ELIX'), delay=0.25, writerargs={'procs': 4, 'limitmb': 128})

    writer = AsyncWriter(ix_searcher(where))
    writer.update_document(**kwargs)
    writer.commit()


# noinspection PyUnusedLocal
def begin_async_commit(app, **extra):
    """
    Does async commit to the Whoosh index so that data would get written appropriately.
    Even though the passed in app does not get used, it has to be there are the first argument: please note.
    :param app: flask app that is necessary to bootstrap the application
    :param extra: some parameters
    :return: None
    """
    write_async(extra.get("result"), where=extra.get("where"))


generated_signals = Namespace()
error_signal_sent = generated_signals.signal("error-sent-signal")
error_signal_sent.connect(
    begin_async_commit, elap
)  # using connect to register a signal callback


# noinspection PyUnresolvedReferences
@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))


import elog.commands  # noqa: F401 E402
from elog.controllers.apiv1 import v1_api  # noqa: F401 E402
from elog.controllers.auth import auth  # noqa: F401 E402

# Business Logic
from elog.controllers.frontend import frontend  # noqa: F401 E402

elap.register_blueprint(frontend)
elap.register_blueprint(v1_api, url_prefix="/api/v1.0")
elap.register_blueprint(auth, url_prefix="/auth")

from elog import errorhandlers  # noqa: F401 E402
from elog.models.profile import User, UserAccess  # noqa: F401 E402
