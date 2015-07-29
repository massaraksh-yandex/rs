from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import registerCommands
from platform.statement.statement import Statement


class Pass(Endpoint):
    def name(self):
        return 'pass'

    def _info(self):
        return ['{path} - ничего не делает, но принимает любые аргументы и опции']

    def _rules(self):
        return [ Statement(['{path} всё_что_угодно'], self.process, lambda p: True) ]

    def process(self, p: Params):
        pass


commands = registerCommands(Pass)
