from platform.params import Params
from platform.utils import makeCommandDict
from platform.command import Command
from platform.endpoint import Endpoint
from src.check_utils import Exist, NotExist
from platform.statement.statement import emptyCommand, singleOptionCommand
from src.project import getProjects
from src.utils import readLineWithPrompt, getProjectPathByName
from os import remove
from src import project


class List(Endpoint):
    def name(self):
        return 'list'

    def _info(self):
        return ['{path} - показывает список проектов']

    def _rules(self):
        return emptyCommand(['{path}'], self.process)

    def process(self, p: Params):
        for k, v in getProjects().items():
            print("project: " + k)


class Show(Endpoint):
    def name(self):
        return 'show'

    def _info(self):
        return ['{path} - показывает информацию о проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        name = p.targets[0].value
        Exist.project(name)
        getProjects().get(name).print()


class Remove(Endpoint):
    def name(self):
        return 'rm'

    def _info(self):
        return ['{path} - удаляет запись о проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        name = p.targets[0].value
        Exist.project(name)
        answer = readLineWithPrompt('Удалить проект {0}? (yes/no)'.format(name), 'no')

        if answer != 'yes':
            print('Отмена...')
            return

        remove(getProjectPathByName(name))

        print('Проект {0} удалён'.format(name))


class Add(Endpoint):
    def name(self):
        return 'add'

    def _info(self):
        return ['{path} - создаёт запись о новом проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        name = p.targets[0].value
        NotExist.project(name)
        prj = project.Project.input(name)
        if prj is not None:
            prj.serialize()
            print('Проект {0} добавлен'.format(prj.name))
        else:
            print('Отмена...')


class Project(Command):
    def name(self):
        return 'project'

    def _info(self):
        return ['{path} - команды управления проектами']

    def _commands(self):
        return makeCommandDict(Add, List, Remove, Show)


module_commands = makeCommandDict(Project)
