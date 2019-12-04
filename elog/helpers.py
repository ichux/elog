from pprint import pprint

from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


class InvalidAuthentication(ValueError):
    """"""


# vars = extract_vars(request.form)

def extract_vars(form):
    _dict = {}
    for key, value in form.items():
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if not key in _dict:
            _dict[key] = value
        elif isinstance(_dict[key], list):
            _dict[key].append(value)
        else:
            _dict[key] = [_dict[key], value]
    return _dict


def prepare_arguments(request_args):
    """Prepare DataTables with default arguments.
    :param request_args: request.args are supplied by flask
    :type request_args: flask dictionary data type
    """
    request_values = dict()
    for key, value in request_args.items():
        try:
            request_values[key] = int(value)
        except ValueError:
            if value in ('true', 'false'):
                request_values[key] = value == 'true'
            else:  # assume string
                request_values[key] = value
    return request_values


def details(obj):
    """
    Does a pretty print of the object representation
    :param obj: the object to be pretty printed
    :return: a pretty print representation
    """
    pprint(vars(obj))

#
# def looked(qs, pagenum, pagelen, locate):
#     # qs = 'Rain* OR subdomain:asch OR address:osun'
#     query = qparser.QueryParser("details", ix_searcher(locate).searcher().schema)
#     query.add_plugin(DateParserPlugin())
#
#     if not pagelen:
#         pagelen = current_app.config['MAX_WHOOSH_SEARCH_RESULTS']
#     pagelen = min(pagelen, current_app.config['MAX_WHOOSH_SEARCH_RESULTS'])
#
#     results = ix_searcher(locate).searcher().search_page(query.parse(qs), pagenum, pagelen, sortedby="date",
#                                                          reverse=True)
#     output = []
#
#     if len(results) > 0:
#         print("Last page: %s" % results.is_last_page())
#         print("Page %d of %d" % (results.pagenum, results.pagecount))
#         print("Shows results %d-%d of %d" % (results.offset + 1, results.offset + results.pagelen + 1, len(results)))
#         # print(dir(results))
#         for hit in results:
#             # print hit.highlights("details")
#             # print hit.highlights("details", hit["details"])
#             # print hit["details"]
#             # print(hit.rank)
#             keeps = {}
#             for key, value in hit.iteritems():
#                 keeps[key] = value
#             output.append(keeps)
#     return {'hits': len(results), 'output': output}  # , 'spent': "%0.04f" % results.runtime
#
#
# def getdoc(qs, locate):
#     results = ix_searcher(locate).searcher().documents(address=qs)
#     for hit in results:
#         print(hit['id'])
#     print ix_searcher(locate).searcher().document(id=u"1")
#
#
# def get_log(qs, locate):
#     results = ix_searcher(locate).searcher().documents(httpmethod=qs)
#     for hit in results:
#         print(hit)
#         # print search_ix(locate).document(id=u"1")
#
# def lookup(qs, page_num, page_len, locate):
#     query = qparser.QueryParser("name", ix_searcher(locate).searcher().schema)
#
#     mf = session.get('mf')
#     if mf and mf == 'y':
#         query = qparser.MultifieldParser(["name", "address"], ix_searcher(locate).searcher().schema)
#
#     '''
#     # qs = 'Rain* OR subdomain:asch OR address:osun'
#     query = qparser.QueryParser("name", search_ix(locate).schema)
#     # searcher.search(query, limit=None, terms=True)
#     '''
#
#     if not page_len:
#         page_len = current_app.config['MAX_WHOOSH_SEARCH_RESULTS']
#     page_len = min(page_len, current_app.config['MAX_WHOOSH_SEARCH_RESULTS'])
#
#     results = ix_searcher(locate).searcher().search_page(query.parse(qs), page_num, page_len)
#     # print(search_ix(locate).correct_query(query.parse(qs), qs, prefix=1))
#     output = []
#
#     if len(results) > 0:
#         print("Last page: %s" % results.is_last_page())
#         print("Page %d of %d" % (results.pagenum, results.pagecount))
#         print("Shows results %d-%d of %d" % (results.offset + 1, results.offset + results.pagelen + 1, len(results)))
#         # print(dir(results))
#         for hit in results:
#             output.append(hit['id'])
#             # print hit.highlights("name")
#             # print hit.highlights("address")
#     return {'hits': len(results), 'output': output}  # , 'spent': "%0.04f" % results.runtime
