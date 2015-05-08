from platform.exception import WrongOptions, WrongTargets
from platform.command import Command, Endpoint
from platform.delimer import checkNoDelimers
from platform.utils import makeCommandDict
from src.workspace import getWorkspaces
from src import workspace


class List(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'list'

    def _help(self):
        return ['{path} - показывает список рабочих окружений',
                '{path}']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def _process(self, p):
        for k, v in getWorkspaces().items():
            print('workspace: ' + k)


class Add(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'add'

    def _help(self):
        return ['{path} - создаёт запись о новом рабочем окружении',
                '{path} рабочее_окружение']

    def _check(self, p):
        checkNoDelimers(p)
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))
        if p.targets[0] in getWorkspaces():
            raise WrongTargets('Проект {0} уже существует'.format(p.targets[0]))

    def _process(self, p):
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
        self.commands = makeCommandDict([Add, List])

    def name(self):
        return 'workspace'

    def _help(self):
        return [pr(self).path() for k, pr in self.commands.items()]

    def _check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('Отсутствуют цели')


    def _process(self, p):
        cmd = p.targets[0]
        v = self.commands[cmd](self)
        v.execute(p.argv[1:])


module_commands = makeCommandDict([Workspace])
