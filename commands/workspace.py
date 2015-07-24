from platform.commands.command import Command
from platform.commands.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.workspace import getWorkspaces
from src import workspace
from src.check_utils import NotExist
from platform.statement.statement import emptyCommand, singleOptionCommand

class List(Endpoint):
    def name(self):
        return 'list'

    def _info(self):
        return ['{path} - показывает список рабочих окружений']

    def _rules(self):
        return emptyCommand(['{path}'], self.process)

    def process(self, p: Params):
        for k, v in getWorkspaces().items():
            print('workspace: ' + k)


class Add(Endpoint):
    def name(self):
        return 'add'

    def _info(self):
        return ['{path} - создаёт запись о новом рабочем окружении']

    def _rules(self):
        return singleOptionCommand(['{path} рабочее_окружение'], self.process)

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

    def _info(self):
        return ['{path} - команды управления рабочими окружениями']

    def _commands(self):
        return makeCommandDict(Add, List)


module_commands = makeCommandDict(Workspace)
