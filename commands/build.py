from platform.statement.rule import Rule
from platform.statement.statement import Statement
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
        return [ Statement(['{path} [--targets=цели] проект',
                            "{space}Для синхронизации используется команда 'send проект'",
                            "{space}Для построения 'make цели -- проект'",
                            '--targets - задаёт цели для построения',
                            '{space}цели по умолчанию: all, install, check',
                            '{space}цели задаются через запятую'], self.deploy,
                           lambda p: Rule(p).empty().delimers()
                                            .check().optionNamesInSet('targets')
                                            .size().equals(p.targets, 1)) ]

    def name(self) -> '':
        return 'deploy'

    def deploy(self, p: Params):
        name = p.targets[0].value
        Exist(self.database).project(name)
        targets = p.options['targets'] or ['all', 'install', 'check']

        self.subcmd(Send).execute([name])
        for i in targets:
            self.subcmd(Make).execute([i, '--', name])


class Build(Command):
    def name(self) -> '':
        return 'build'

    def _info(self):
        return ['{path} - составные высокоуровневые команды для упрощения процесса разработки']

    def _commands(self) -> {}:
        return registerCommands(Deploy)


commands = registerCommands(Build)
