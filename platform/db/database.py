import os
from os.path import join, basename, splitext
from abc import ABCMeta, abstractmethod
from glob import glob
from os import remove
import json


class Database(metaclass=ABCMeta):
    def __init__(self, config, settings):
        self.settings = settings
        self.config = config

    def _select(self, what, path, type):
        ret = {}
        for name in glob(join(path, what+'.json')):
            with open(name, 'r') as f:
                name = basename(splitext(name)[0])
                ret[name] = type(**json.load(f))
        return ret

    def _objPath(self, dir, name):
        return join(dir, os.path.splitext(name)[0] + '.json')

    @abstractmethod
    def _getDirByType(self, object):
        pass

    def update(self, object):
        path = self._getDirByType(object.__class__)

        with open(self._objPath(path, object.name), 'w') as f:
            f.write(repr(object))

    def remove(self, object):
        path = self._getDirByType(object.__class__)
        remove(join(path, object.name+'.json'))

    def select(self, name, type):
        path = self._getDirByType(type)
        return self._select(name, path, type)

    def selectone(self, name, type):
        return self.select(name, type)[name]

