from platform.command import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict


class Pass(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'pass'

    def _help(self):
        return ['{path} - ничего не делает, но принимает любые аргументы и опции',
                '{path} опции']

    def _checkNew(self):
        return [lambda p: None]

    def _check(self, p: Params):
        pass

    def _process(self, p: Params):
        pass

module_commands = makeCommandDict([Pass])
