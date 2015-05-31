from src.settings import Settings
from glob import glob
from os.path import join, basename, splitext
from src.utils import getWorkspacePathByName, getExcludeFileArg, readLineWithPrompt
from src.sync import SyncData
import json

class Workspace:
    def __init__(self, name, map):
        self.name = name
        self.host = map['host']
        self.root = map['root']
        self.include = map['include']
        self.src = map['src']
        self.etc = map['etc']

    @staticmethod
    def input(name):
        map = {}
        map['host'] = readLineWithPrompt('Хост', 'wmidevaddr')
        map['root'] = readLineWithPrompt('Корень', '~/ws')
        map['include'] = readLineWithPrompt('Заголовочные файлы', join(map['root'], 'include'))
        map['src'] = readLineWithPrompt('Исходный код', join(map['root'], 'src'))
        map['etc'] = readLineWithPrompt('Конфигурационные файлы', join(map['root'], 'etc'))

        ws = Workspace(name, map)
        if readLineWithPrompt('Всё верно (yes/no)', 'no') != 'yes':
            return None
        else:
            return ws

    def toSyncData(self, p = None) -> SyncData:
        path = self.src if p is None else p
        return SyncData(path, self.host, path, getExcludeFileArg(path))

    def serialize(self):
        with open(getWorkspacePathByName(self.name), 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def print(self):
        print('Название: ' + self.name)
        print('Хост: ' + self.host)
        print('Корень: ' + self.root)
        print('Заголовочные файлы: ' + self.include)
        print('Исходный код: ' + self.src)
        print('Конфигурационные файлы: ' + self.etc)


def getWorkspaces():
    ret = {}
    for name in glob(join(Settings().WORKSPACES_DIR, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Workspace(name, json.load(f))

    return ret
