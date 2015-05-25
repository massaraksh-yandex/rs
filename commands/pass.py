from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict


class Pass(Endpoint):
    def name(self):
        return 'pass'

    def _help(self):
        return ['{path} - ничего не делает, но принимает любые аргументы и опции',
                '{path} всё_что_угодно']

    def _rules(self):
        return [lambda p: self.process]

    def process(self, p: Params):
        pass


module_commands = makeCommandDict(Pass)
