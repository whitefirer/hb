# coding=utf-8
# author=whitefirer

from server import app, api
from flask import render_template
from flask_restplus import apidoc
from werkzeug.wsgi import DispatcherMiddleware

_app = DispatcherMiddleware(
        app, {
        }
    )

if __name__ == '__main__':
    port = 9102
    debug = True
    @api.documentation
    def disable_document():
        if not debug:
            #return api.render_root()
            return render_template('/index/')
        return apidoc.ui_for(api)

    #app.run(debug=debug, host='0.0.0.0', port=9102)
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
