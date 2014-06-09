# -*- coding:utf-8 -*-
def _getTarget():
    from hmm import StringExchange
    return StringExchange


def _makeOne(*args, **kwargs):
    return _getTarget()(*args, **kwargs)


def test_it():
    from hmm import default_emiter_factory

    target = _makeOne(default_emiter_factory)
    xs = [target.subscribe("xxx"), "hello", "this is", target.subscribe("xxx"), "www"]

    publisher = target.publisher("xxx")
    publisher.publish("@.@")
    content = "".join(xs)

    result = target.emit(content)
    assert result == "@.@hellothis is@.@www"


def test_funcall():
    from hmm import function_call_emitter

    target = _makeOne((lambda name: function_call_emitter))
    fmt = """f(x, {}, y, z)""".format(target.subscribe("args"))

    publisher = target.publisher("args")
    publisher.publish("a")
    publisher.publish("b\n")
    publisher.publish("c\n")

    result = target.emit(fmt)

    assert result == "f(x, a, b, c, y, z)"

