from platform.params import Params
from platform.utils import makeCommandDict
from platform.command import Command
from platform.endpoint import Endpoint
from src.check_utils import singleOptionCommand, Exist, NotExist, emptyCommand
from src.project import getProjects
from src.utils import readLineWithPrompt, getProjectPathByName
from os import remove
from src import project


class List(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'list'

    def _help(self):
        return ['{path} - показывает список проектов',
                '{path}']

    def _rules(self):
        return emptyCommand(self.process)

    def process(self, p: Params):
        for k, v in getProjects().items():
            print("project: " + k)


class Show(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'show'

    def _help(self):
        return ['{path} - показывает информацию о проекте',
                '{path} название_проекта']

    def _rules(self):
        return singleOptionCommand(self.process)

    def process(self, p: Params):
        name = p.targets[0]
        Exist.project(name)
        getProjects().get(name).print()


class Remove(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'rm'

    def _help(self):
        return ['{path} - удаляет запись о проекте',
                '{path} название_проекта']

    def _rules(self):
        return singleOptionCommand(self.process)

    def process(self, p: Params):
        name = p.targets[0]
        Exist.project(name)
        answer = readLineWithPrompt('Удалить проект {0}? (yes/no)'.format(name), 'no')

        if answer != 'yes':
            print('Отмена...')
            return

        remove(getProjectPathByName(name))

        print('Проект {0} удалён'.format(name))


class Add(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'add'

    def _help(self):
        return ['{path} - создаёт запись о новом проекте',
                '{path} название_проекта']

    def _rules(self):
        return singleOptionCommand(self.process)

    def process(self, p: Params):
        name = p.targets[0]
        NotExist.project(name)
        prj = project.Project.input(name)
        if prj is not None:
            prj.serialize()
            print('Проект {0} добавлен'.format(prj.name))
        else:
            print('Отмена...')


class Project(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'project'

    def _commands(self):
        return makeCommandDict([Add, List, Remove, Show])


module_commands = makeCommandDict([Project])
