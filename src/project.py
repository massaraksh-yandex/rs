from src.settings import Settings
from src.utils import getProjectPathByName, getExcludeFile, readLineWithPrompt
from os.path import basename, join, splitext
from src.sync import SyncData
from glob import glob
from src.workspace import getWorkspaces
import json

class Project:
    name = ''
    path = ''
    workspace = ''
    project_type = ''

    def __init__(self, name, map):
        self.name = name
        self.path = map['path']
        self.workspace = map['workspace']
        self.project_type = map['project_type']

    @staticmethod
    def input(name):
        map = {}
        default_workspace = 'wmi_default'
        ws = getWorkspaces()[default_workspace]
        map['path'] = readLineWithPrompt('Родительская папка', ws.src)
        map['project_type'] = readLineWithPrompt('Тип проекта', 'qtcreator_import')
        map['workspace'] = readLineWithPrompt('Рабочее окружение', default_workspace)

        project = Project(name, map)
        if readLineWithPrompt('Всё верно (yes/no)', 'no') != 'yes':
            return None
        else:
            return project

    def toSyncData(self) -> SyncData:
        path = join(self.path, self.name)
        ws = getWorkspaces()[self.workspace]
        return SyncData(path, ws.host, join(ws.src, self.name), getExcludeFile(path))

    def serialize(self):
        with open(getProjectPathByName(self.name), 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def print(self):
        print('Название: ' + self.name)
        print('Родительская папка: ' + self.path)
        print('Тип проекта: ' + self.project_type)
        print('Рабочее окружение: ' + self.workspace)

def getProjects(path = Settings.REMOTES_DIR):
    ret = {}
    for name in glob(join(path, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Project(name, json.load(f))

    return ret