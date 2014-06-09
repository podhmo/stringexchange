stringexchange
========================================

no pyramid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from stringexchange import make_exchange, function_call_emitter

    exchange = make_exchange(function_call_emitter)

    template = """f(a, {}, b)""".format(exchange.subscribe("args"))
    p = exchange.publisher("args")

    p.publish("x")
    p.publish("y\n")
    p.publish("z")

    output = exchange.emit(template)
    assert output == "f(a, x, y, z, b)"

on pyramid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # -*- coding:utf-8 -*-
    ## onpyramid.py
    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    import os.path


    def top_view(request):
        js = request.string_exchange.publisher("js")
        return {"js": js}


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


.. code:: html

    ## top.html
    <html>
    <head>
    ${request.string_exchange.subscribe("js", "newline")}
    </head>
    <body>

    <!-- foo widget -->
    <% js.publish('<script src="foo.js"></script>') %>
    <h1>foo</h1>
    foo content

    <!-- boo widget -->
    <% js.publish('<script src="boo.js"></script>') %>
    <h1>boo</h1>
    <ul>
    <li>boo0</li>
    <li>boo1</li>
    <li>boo2</li>
    </ul>

    </body>
    </html>

.. code:: bash

    $ python demo/onpyramid.py &
    $ curl http://localhost:8080
    <html>
    <head>
    <script src="foo.js"></script>
    <script src="boo.js"></script>
    </head>
    <body>

    <!-- foo widget -->

    <h1>foo</h1>
    foo content

    <!-- boo widget -->

    <h1>boo</h1>
    <ul>
    <li>boo0</li>
    <li>boo1</li>
    <li>boo2</li>
    </ul>

    </body>
    </html>
