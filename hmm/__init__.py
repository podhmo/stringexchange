# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from .interfaces import IEmitter
from zope.interface import provider
import hashlib
from collections import defaultdict


class Gensym(object):
    def __init__(self, i=0):
        self.i = i

    def __call__(self):
        v = "g!{}".format(hashlib.sha1(bytes(self.i)).hexdigest())
        self. i += 1
        return v


@provider(IEmitter)
def join_emitter(hashval, xs, string):
    return string.replace(hashval, "".join(xs))


@provider(IEmitter)
def function_call_emitter(hashval, xs, string):
    return string.replace(hashval, ", ".join(x.strip() for x in xs))


def default_emiter_factory(name):
    return join_emitter


class EmitterFactory(object):
    def __init__(self, request):
        self.request = request

    def __call__(self, name):
        q = self.request.registry.queryUtility
        return q(IEmitter, name=name, default=join_emitter)


class StringExchange(object):
    def __init__(self, emitter_factory=default_emiter_factory):
        self.emitter_factory = emitter_factory
        self.hash_map = {}
        self.contents_map = defaultdict(list)
        self.gensym = Gensym()
        self.publishers = {}
        self.emit_name_map = {}

    def subscribe(self, k, emit_name=""):
        try:
            return self.hash_map[k]
        except KeyError:
            v = self.hash_map[k] = self.gensym()
            setattr(self, k, v)
            self.emit_name_map[k] = emit_name
            return v

    def emit(self, string):
        for k in self.hash_map:
            hash_val = self.hash_map[k]
            contents = self.contents_map[k]
            name = self.emit_name_map[k]
            emitter = self.emitter_factory(name)
            string = emitter(hash_val, contents, string)
        return string

    def publisher(self, k):
        try:
            return self.publishers[k]
        except KeyError:
            p = self.publishers[k] = Publisher(self.contents_map, k)
            return p

    def talk(self, k, message):
        self.contents_map[k].append(message)


class Publisher(object):
    def __init__(self, strings, k):
        self.buf = strings[k]
        self.k = k

    def publish(self, message):
        return self.buf.append(message)


class StringExchangeTweenFactory(object):
    def __init__(self, handler, setting):
        self.handler = handler

    def __call__(self, request):
        response = self.handler(request)
        if response.status_int != 200:
            return response

        if not (response.content_type and
                response.content_type.lower() in ['text/html', 'text/xml']):
            return response

        response_text = response.text
        response.text = ""
        response.write(request.string_exchange.emit(response_text))
        return response


def get_string_exchange(request):
    return StringExchange(EmitterFactory(request))


def add_emitter(config, emitter, name=""):
    config.registry.registerUtility(emitter, IEmitter, name=name)


def includeme(config):
    config.add_tween("hmm.StringExchangeTweenFactory")
    config.add_request_method(get_string_exchange, "string_exchange", reify=True)
    config.add_directive("add_emitter", add_emitter)
    config.add_emitter(join_emitter)
    config.add_emitter(function_call_emitter, "call")
