from whoosh.fields import (  # type: ignore
    DATETIME,
    ID,
    NUMERIC,
    STORED,
    TEXT,
    SchemaClass,
)


class ErrorLogsSchema(SchemaClass):
    # sortable=True means Whoosh stores per-document values for that field in a column
    id = ID(stored=True, unique=True)
    ip = TEXT(stored=True, sortable=True)

    code = NUMERIC(stored=True)
    errormsg = TEXT(stored=True)
    errortype = TEXT(stored=True)
    httpmethod = TEXT(stored=True, sortable=True)
    referrer = TEXT(stored=True, sortable=True)
    requestpath = TEXT(stored=True, sortable=True)
    useragent = TEXT(stored=True, sortable=True)
    userbrowser = TEXT(stored=True, sortable=True)
    userbrowserversion = TEXT(stored=True)
    userplatform = TEXT(stored=True, sortable=True)
    date = DATETIME(sortable=True)

    # stored values but are not searched upon. These can fill up the index quickly
    postvalues = STORED()
    requestargs = STORED()
    errortraceback = STORED()
    when = STORED()
