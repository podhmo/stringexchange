# -*- coding:utf-8 -*-
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import os.path


def top_view(request):
    js = request.string_exchange.publisher("js")
    css = request.string_exchange.publisher("css")
    return {"css": css, "js": js}


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    settings = {"mako.directories": here,
                "pyramid.reload_templates": True}
    config = Configurator(settings=settings)

    config.include("pyramid_mako")
    config.include("stringexchange")  # !!
    config.add_mako_renderer(".html")

    config.add_route('top', '/')
    config.add_view(top_view, route_name='top', renderer="top.html")

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


