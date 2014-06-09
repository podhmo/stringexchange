# -*- coding:utf-8 -*-
from stringexchange import make_exchange, function_call_emitter

exchange = make_exchange(function_call_emitter)

template = """f(a, {}, b)""".format(exchange.subscribe("args"))
p = exchange.publisher("args")

p.publish("x")
p.publish("y\n")
p.publish("z")

output = exchange.emit(template)
assert output == "f(a, x, y, z, b)"
