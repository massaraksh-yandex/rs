from src.settings import Settings, getProjectPathByName
from os.path import basename, join, splitext
from glob import glob
import json

class Project:
    name = None
    path = None
    remote_path = None
    host = None
    project_type = None

    def __init__(self, name = '', map = {}):
        self.name = name
        for key, value in map.items():
            setattr(self, key, value)


def serializeProject(pr: Project):
    with open(getProjectPathByName(pr.name), 'w') as f:
        json.dump(pr.__dict__, f)


def printProject(pr: Project):
    print('Название: ' + pr.name)
    print('Путь: ' + pr.path)
    print('Хост: ' + pr.host)
    print('Тип проекта: ' + pr.project_type)

def getProjects(path = Settings.REMOTES_DIR):
    ret = {}
    for name in glob(join(path, '*.json')):
        with open(name, 'r') as f:
            name = basename(splitext(name)[0])
            ret[name] = Project(name, json.load(f))

    return ret