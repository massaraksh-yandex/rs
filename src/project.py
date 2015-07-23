from src.config import Config
from src.settings import Settings
from src.utils import getProjectPathByName, getExcludeFileArg, readLineWithPrompt
from os.path import basename, join, splitext
from src.sync import SyncData
from glob import glob
from src.workspace import getWorkspaces
import json

class Project:
    def __init__(self, name, map):
        self.name = name
        self.path = map['path']
        self.workspace = map['workspace']
        self.project_type = map['project_type']

    @staticmethod
    def input(name):
        map = {}
        dw = Config.instance.defaultWorkspace
        ws = getWorkspaces()[dw]
        map['path'] = readLineWithPrompt('Родительская папка', ws.src)
        map['project_type'] = readLineWithPrompt('Тип проекта', 'qtcreator_import')
        map['workspace'] = readLineWithPrompt('Рабочее окружение', dw)

        project = Project(name, map)
        if readLineWithPrompt('Всё верно (yes/no)', 'no') != 'yes':
            return None
        else:
            return project

    def toSyncData(self, forceWs = None) -> SyncData:
        path = join(self.path, self.name)
        ws = getWorkspaces()[self.workspace if forceWs is None else forceWs]
        return SyncData(path, ws.host, join(ws.src, self.name), getExcludeFileArg(path))

    def serialize(self):
        with open(getProjectPathByName(self.name), 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def print(self):
        print('Название: ' + self.name)
        print('Родительская папка: ' + self.path)
        print('Тип проекта: ' + self.project_type)
        print('Рабочее окружение: ' + self.workspace)

def getProjects():
    ret = {}
    for name in glob(join(Settings().REMOTES_DIR, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Project(name, json.load(f))

    return ret