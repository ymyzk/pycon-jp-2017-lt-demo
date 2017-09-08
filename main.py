import time

import bottle
from bottle import request


app = bottle.default_app()


def mock_db_access(n):
    result = []
    for i in range(n):
        time.sleep(0.1)
        result.append(f"Item: {i}")
    return result


@app.route("/")
def index():
    size = int(request.query.get("size", "10"))
    items = mock_db_access(size)
    items_str = "\n".join(items)
    time.sleep(0.3)
    return "Hello, world!\n" + items_str


# Profile w/o filtering
# from wsgi_lineprof.middleware import LineProfilerMiddleware
# app = LineProfilerMiddleware(app)

# Profile w/ filtering
from wsgi_lineprof.filters import FilenameFilter, TotalTimeSorter
from wsgi_lineprof.middleware import LineProfilerMiddleware
filters = [
    FilenameFilter("main.py"),
    TotalTimeSorter(),
]
app = LineProfilerMiddleware(app, filters=filters)


bottle.run(app=app, reloader=True)
