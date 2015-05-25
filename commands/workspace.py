from platform.command import Command
from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.workspace import getWorkspaces
from src import workspace
from src.check_utils import singleOptionCommand, emptyCommand, NotExist


class List(Endpoint):
    def name(self):
        return 'list'

    def _help(self):
        return ['{path} - показывает список рабочих окружений',
                '{path}']

    def _rules(self):
        return emptyCommand(self.process)

    def process(self, p: Params):
        for k, v in getWorkspaces().items():
            print('workspace: ' + k)


class Add(Endpoint):
    def name(self):
        return 'add'

    def _help(self):
        return ['{path} - создаёт запись о новом рабочем окружении',
                '{path} рабочее_окружение']

    def _rules(self):
        return singleOptionCommand(self.process)

    def process(self, p: Params):
        name = p.targets[0]
        NotExist.workspace(name)
        ws = workspace.Workspace.input(name)
        if ws is not None:
            ws.serialize()
            print('Рабочее окружение {0} добавлено'.format(ws.name))
        else:
            print('Отмена...')


class Workspace(Command):
    def name(self):
        return 'workspace'

    def _commands(self):
        return makeCommandDict(Add, List)


module_commands = makeCommandDict(Workspace)
