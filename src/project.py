from src.settings import Settings
from src.utils import getProjectPathByName, getExcludeFile, readLineWithPrompt
from os.path import basename, join, splitext
from src.sync import SyncData
from glob import glob
import json

class Project:
    name = ''
    path = ''
    remote_path = ''
    host = ''
    project_type = ''

    def __init__(self, name = '', map = {}):
        self.name = name
        for key, value in map.items():
            setattr(self, key, value)

    @staticmethod
    def input(name):
        project = Project(name)

        project.path = readLineWithPrompt('Путь', '/home/massaraksh/ws')
        project.host = readLineWithPrompt('Хост', 'wmidevaddr')
        project.project_type = readLineWithPrompt('Тип проекта', 'qtcreator_import')
        answer = readLineWithPrompt('Всё верно (yes/no)', 'no')

        if answer != 'yes':
            return None
        else:
            return project

    def toSyncData(self) -> SyncData:
        path = join(self.path, self.name)
        return SyncData(path, self.host, path, getExcludeFile(path))

    def serialize(self):
        with open(getProjectPathByName(self.name), 'w') as f:
            json.dump(self.__dict__, f)

    def print(self):
        print('Название: ' + self.name)
        print('Путь: ' + self.path)
        print('Хост: ' + self.host)
        print('Тип проекта: ' + self.project_type)

def getProjects(path = Settings.REMOTES_DIR):
    ret = {}
    for name in glob(join(path, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Project(name, json.load(f))

    return ret