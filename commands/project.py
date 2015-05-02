from src.repo import getProjects, serializeProject, printProject
from src import repo
from platform.exception import WrongOptions, WrongTargets
from platform.command import Command
from platform.delimer import checkNoDelimers
from src.utils import readLineWithPrompt
from os import remove
from src.settings import getProjectPathByName


class List(Command):
    def help(self):
        print('list - показывает список проектов')
        print('rs project list [--help]')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def process(self, p):
        for k, v in getProjects().items():
            print("project: " + k)


class Show(Command):
    def help(self):
        print('show проект - показывает информацию о проекте')
        print('rs project show [проект]')
        print('rs project show --help')
        print('[проект] - название проекта')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] not in getProjects():
            raise WrongTargets('Проект {0} не существует'.format(p.targets[0]))

    def process(self, p):
        a = getProjects().get(p.targets[0])
        #print (str(a.))
        printProject(a)


class Remove(Command):
    def help(self):
        print('remove проект - удаляет запись о проекте')
        print('rs project remove [проект]')
        print('rs project remove --help')
        print('[проект] - название проекта')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] not in getProjects():
            raise WrongTargets('Проект {0} не существует'.format(p.targets[0]))

    def process(self, p):
        name = p.targets[0]
        answer = readLineWithPrompt('Удалить проект {0}? (yes/no)'.format(name), 'no')

        if answer != 'yes':
            print('Отмена...')
            return

        remove(getProjectPathByName(name))

        print('Проект {0} удалён'.format(name))


class Create(Command):
    def help(self):
        print('create проект - создаёт запись о новом проекте')
        print('rs project create [проект]')
        print('rs project create --help')
        print('[проект] - название проекта')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] in getProjects():
            raise WrongTargets('Проект {0} уже существует'.format(p.targets[0]))

    def process(self, p):
        project = repo.Project(p.targets[0])

        project.path = readLineWithPrompt('Путь', '/home/massaraksh/ws')
        project.host = readLineWithPrompt('Хост', 'wmidevaddr')
        project.project_type = readLineWithPrompt('Тип проекта', 'qtcreator_import')
        answer = readLineWithPrompt('Всё верно (yes/no)', 'no')

        if answer != 'yes':
            print('Отмена...')
            return

        serializeProject(project)
        print('Проект {0} добавлен'.format(project.name))


class Project(Command):
    commands = {'create': Create, 'list': List, 'rm': Remove, 'show': Show}

    def help(self):
        print('rs project create')
        print('rs project list')

    def check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('Отсутствуют цели')


    def process(self, p):
        cmd = p.targets[0]
        v = self.commands[cmd]()
        v.execute(p.argv[1:])


module_commands = {'project': Project}
