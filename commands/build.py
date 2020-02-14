from platform.statement.rule import Rule
from platform.statement.statement import Statement
from platform.commands.endpoint import Endpoint
from platform.commands.command import Command
from platform.utils.utils import registerCommands
from platform.params.params import Params
from src.db.project import Project
from src.db.workspace import Workspace
from src.utils.check import *
from commands.get_or_send import Send
from commands.make import Make


class Yamake(Endpoint):
    def _info(self) -> []:
        return ['{path} - отсылает проект на сервер и запускает ya make']

    def _rules(self) -> []:
        return [Statement(['{path} [--t] [--ws] проект',
                           "{space}Для синхронизации используется команда 'send проект'",
                           "{space}Для построения запуск yamake на удалённой тачке",
                           '--ws - имя воркспейса',
                           '--path - папка в аркадии первого уровня',
                           '--t - запуск тестов'], self.yamake,
                          lambda p: Rule(p).empty().delimers()
                                           .check().optionNamesInSet('nohl', 't', 'tt', 'ttt', 'ws',
                                                                     'add_tests', 'add_builds')
                                           .size().equals(p.targets, 1))]

    def name(self) -> '':
        return 'yamake'

    def yamake(self, p: Params):
        name = p.targets[0].value
        Exist(self.database).project(name)
        project: Project = self.database.projects()[name]

        if 'ws' in p.options:
            ws: Workspace = self.database.workspaces()[p.options['ws']]
        else:
            ws: Workspace = self.database.workspaces()[project.workspace]

        self.subcmd(Send).execute([name, f'--ws={ws.name}'])
        self.subcmd(Make).execute(p.argv)


class Build(Command):
    def name(self) -> '':
        return 'build'

    def _info(self):
        return ['{path} - составные высокоуровневые команды для упрощения процесса разработки']

    def _commands(self) -> {}:
        return registerCommands(Yamake)


commands = registerCommands(Build)
