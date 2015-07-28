from platform.commands.command import Command
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import makeCommandDict
from src.db import workspace
from src.utils.check import NotExist
from platform.statement.statement import emptyCommand, singleOptionCommand

class List(Endpoint):
    def name(self):
        return 'list'

    def _info(self):
        return ['{path} - показывает список рабочих окружений']

    def _rules(self):
        return emptyCommand(['{path}'], self.process)

    def process(self, p: Params):
        for k, v in self.database.workspaces().items():
            print('workspace: ' + k)


class Add(Endpoint):
    def name(self):
        return 'add'

    def _info(self):
        return ['{path} - создаёт запись о новом рабочем окружении']

    def _rules(self):
        return singleOptionCommand(['{path} рабочее_окружение'], self.process)

    def process(self, p: Params):
        name = p.targets[0].value
        NotExist(self.database).workspace(name)
        ws = workspace.inputWorkspace(name)
        if ws is not None:
            self.database.update(ws)
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
