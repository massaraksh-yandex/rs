from platform.check import singleOptionCommand
from platform.endpoint import Endpoint
from platform.command import Command
from platform.utils import makeCommandDict
from platform.params import Params
from src.check_utils import *
from commands.send import Send
from commands.make import Make


class Deploy(Endpoint):
    def _help(self) -> []:
        return ['{path} - отсылает проект на сервер и компилирует его',
                '{path} проект',
                '{space}Для синхронизации используется команда send проект',
                '{space}Для построения make all install -- проект']

    def _rules(self) -> []:
        return singleOptionCommand(self.deploy)

    def name(self) -> '':
        return 'deploy'

    def deploy(self, p: Params):
        name = p.targets[0].value
        Exist.project(name)
        Send(self).execute([name])
        Make(self).execute(['all', 'install', '--', name])
        Make(self).execute(['check', '--', name])


class Build(Command):
    def name(self) -> '':
        return 'build'

    def _commands(self) -> {}:
        return makeCommandDict(Deploy)


module_commands = makeCommandDict(Build)
