# -*- coding:utf-8 -*-
def _getTarget():
    from hmm import Emitter
    return Emitter


def _makeOne(*args, **kwargs):
    return _getTarget()(*args, **kwargs)


def test_it():
    target = _makeOne()
    xs = [target.xxx, "hello", "this is", target.xxx, "www"]

    publisher = target.publisher("xxx")
    publisher.publish("@.@")
    content = "".join(xs)

    result = target.emit(content)
    assert result == "@.@hellothis is@.@www"

