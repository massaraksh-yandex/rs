from src.settings import Settings
from glob import glob
from os.path import join, basename, splitext
from src.utils import getWorkspacePathByName, getExcludeFile, readLineWithPrompt
from src.sync import SyncData
import json

class Workspace:
    name = ''
    host = ''
    root = ''
    include = ''
    src = ''

    def __init__(self, name = '', map = {}):
        self.name = name
        for key, value in map.items():
            setattr(self, key, value)

    @staticmethod
    def input(name):
        ws = Workspace(name)

        ws.host = readLineWithPrompt('Хост', 'wmidevaddr')
        ws.root = readLineWithPrompt('Корень', '/home/massaraksh/ws')
        ws.include = readLineWithPrompt('Заголовочные файлы', '')
        ws.src = readLineWithPrompt('Исходный код', '')

        answer = readLineWithPrompt('Всё верно (yes/no)', 'no')

        if answer != 'yes':
            return None
        else:
            return ws

    def toSyncData(self, p = None) -> SyncData:
        path = self.src if p is None else p
        return SyncData(path, self.host, path, getExcludeFile(path))

    def serialize(self):
        with open(getWorkspacePathByName(self.name), 'w') as f:
            json.dump(self.__dict__, f)

    def print(self):
        print('Название: ' + self.name)
        print('Хост: ' + self.host)
        print('Корень: ' + self.root)
        print('Заголовочные файлы: ' + self.include)
        print('Исходный код: ' + self.src)


def getWorkspaceByHostAndPath(host, path) -> Workspace:
    f = lambda x: x.host == host and x.root == path
    return filter(f, list(getWorkspaces()))

def getWorkspaces(path = Settings.WORKSPACES_DIR):
    ret = {}
    for name in glob(join(path, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Workspace(name, json.load(f))

    return ret
