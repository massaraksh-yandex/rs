from platform.statement.statement import singleOptionCommand
from platform.commands.endpoint import Endpoint
from platform.commands.command import Command
from platform.utils.utils import registerCommands
from platform.params.params import Params
from src.utils.check import *
from commands.send import Send
from commands.make import Make


class Deploy(Endpoint):
    def _info(self) -> []:
        return ['{path} - отсылает проект на сервер и компилирует его']

    def _rules(self) -> []:
        return singleOptionCommand(['{path} проект',
                                    '{space}Для синхронизации используется команда send проект',
                                    '{space}Для построения make all install -- проект'],
                                   self.deploy)

    def name(self) -> '':
        return 'deploy'

    def deploy(self, p: Params):
        name = p.targets[0].value
        Exist(self.database).project(name)
        self.subcmd(Send).execute([name])
        self.subcmd(Make).execute(['all', 'install', '--', name])
        self.subcmd(Make).execute(['check', '--', name])


class Build(Command):
    def name(self) -> '':
        return 'build'

    def _info(self):
        return ['{path} - составные высокоуровневые команды для упрощения процесса разработки']

    def _commands(self) -> {}:
        return registerCommands(Deploy)


commands = registerCommands(Build)
