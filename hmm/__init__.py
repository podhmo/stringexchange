# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import hashlib
from collections import defaultdict


class Gensym(object):
    def __init__(self, i=0):
        self.i = i

    def __call__(self):
        v = "g!{}".format(hashlib.sha1(bytes(self.i)).hexdigest())
        self. i += 1
        return v


class Emitter(object):
    def __init__(self):
        self.mapping = {}
        self.strings = defaultdict(list)
        self.gensym = Gensym()
        self.publishers = {}

    def __getattr__(self, k):
        v = self.mapping[k] = self.gensym()
        setattr(self, k, v)
        return v

    def publisher(self, k):
        try:
            return self.publishers[k]
        except KeyError:
            p = self.publishers[k] = Publisher(self.strings, k)
            return p

    def emit(self, string):
        for k in self.mapping:
            hashval = self.mapping[k]
            string = string.replace(hashval, "".join(self.strings[k]))
        return string

    def talk(self, k, message):
        self.strings[k].append(message)


class Publisher(object):
    def __init__(self, strings, k):
        self.buf = strings[k]
        self.k = k

    def publish(self, message):
        return self.buf.append(message)
