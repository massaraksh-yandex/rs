from platform.utils.utils import readLineWithPrompt
import json

class Project:
    def __init__(self, name, path, workspace, project_type):
        self.name = name
        self.path = path
        self.workspace = workspace
        self.project_type = project_type

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '\n'.join(['Название: {name}',
                          'Родительская папка: {path}',
                          'Тип проекта: {project_type}',
                          'Рабочее окружение: {workspace}'])\
            .format(**self.__dict__)


def inputProject(name, database):
    dw = database.config.defaultWorkspace
    ws = database.workspaces()[dw]
    path = readLineWithPrompt('Родительская папка', ws.src)
    workspace = readLineWithPrompt('Рабочее окружение', dw)
    project_type = readLineWithPrompt('Тип проекта', 'qtcreator_import')

    project = Project(name, path, workspace, project_type)
    if readLineWithPrompt('Всё верно (yes/no)', 'no') != 'yes':
        return None
    else:
        return project
