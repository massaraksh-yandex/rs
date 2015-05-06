from platform.exception import WrongOptions, WrongTargets
from platform.command import Command
from platform.delimer import checkNoDelimers
from src.workspace import getWorkspaces
from src import workspace


class List(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'list'

    def help(self):
        print('list - показывает список рабочих окружений')
        print('rs workspace list [--help]')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def process(self, p):
        for k, v in getWorkspaces().items():
            print('workspace: ' + k)


class Add(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'add'

    def help(self):
        print('add [рабочее окружение] - создаёт запись о новом рабочем окружении')
        print('rs workspace add [рабочее окружение]')
        print('rs workspace add --help')
        print('[рабочее окружение] - название проекта')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] in getWorkspaces():
            raise WrongTargets('Проект {0} уже существует'.format(p.targets[0]))

    def process(self, p):
        ws = workspace.Workspace.input(p.targets[0])

        if ws is not None:
            ws.serialize()
            print('Рабочее окружение {0} добавлено'.format(ws.name))
        else:
            print('Отмена...')



class Workspace(Command):
    commands = None

    def __init__(self, parent):
        super().__init__(parent)
        self.commands = {'add': Add, 'list': List}

    def name(self):
        return 'workspace'

    def help(self):
        print('rs workspace add')
        print('rs workspace list')

    def check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('Отсутствуют цели')


    def process(self, p):
        cmd = p.targets[0]
        v = self.commands[cmd](self)
        v.execute(p.argv[1:])


module_commands = {'workspace': Workspace}
