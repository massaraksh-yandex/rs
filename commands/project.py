from platform.utils import makeCommandDict
from src.project import getProjects
from platform.exception import WrongOptions, WrongTargets
from platform.command import Command, Endpoint
from platform.delimer import checkNoDelimers
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
                '{path} --help']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def _process(self, p):
        for k, v in getProjects().items():
            print("project: " + k)


class Show(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'show'

    def _help(self):
        return ['{path} проект - показывает информацию о проекте',
                '{path} [проект]',
                '{path} --help',
                '[проект] - название проекта']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] not in getProjects():
            raise WrongTargets('Проект {0} не существует'.format(p.targets[0]))

    def _process(self, p):
        getProjects().get(p.targets[0]).print()


class Remove(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'rm'

    def _help(self):
        return ['{path} проект - удаляет запись о проекте',
                '{path} [проект]',
                '{path} --help',
                '[проект] - название проекта']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] not in getProjects():
            raise WrongTargets('Проект {0} не существует'.format(p.targets[0]))

    def _process(self, p):
        name = p.targets[0]
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
        return ['{path} проект - создаёт запись о новом проекте',
                '{path} [проект]',
                '{path} --help',
                '[проект] - название проекта']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] in getProjects():
            raise WrongTargets('Проект {0} уже существует'.format(p.targets[0]))

    def _process(self, p):
        prj = project.Project.input(p.targets[0])

        if prj is not None:
            prj.serialize()
            print('Проект {0} добавлен'.format(prj.name))
        else:
            print('Отмена...')


class Project(Command):
    commands = None

    def __init__(self, parent):
        super().__init__(parent)
        self.commands = makeCommandDict([Add, List, Remove, Show])

    def name(self):
        return 'project'

    def _help(self):
        return [pr(self).path() for k, pr in self.commands.items()]

    def _check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('Отсутствуют цели')


    def _process(self, p):
        cmd = p.targets[0]
        v = self.commands[cmd](self)
        v.execute(p.argv[1:])


module_commands = makeCommandDict([Project])
