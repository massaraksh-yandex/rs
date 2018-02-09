from os.path import join
from platform.params.delimer import DoubleDelimer
from platform.statement.rule import Rule
from platform.statement.statement import Statement
from platform.commands.endpoint import Endpoint
from platform.commands.command import Command
from platform.execute.run import run
from platform.utils.utils import registerCommands
from platform.params.params import Params
from src.db.workspace import Workspace
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
                            '{space}цели задаются через запятую',
                            '--path - в этой папке будет происходить сборка'], self.deploy,
                           lambda p: Rule(p).empty().delimers()
                                            .check().optionNamesInSet('targets', 'path')
                                            .size().equals(p.targets, 1)) ]

    def name(self) -> '':
        return 'deploy'

    def deploy(self, p: Params):
        name = p.targets[0].value
        Exist(self.database).project(name)
        targets = p.options['targets'] or 'all,install,check'

        path = p.options['path']

        self.subcmd(Send).execute([name])
        for i in targets.split(','):
            if (path is not None):
                self.subcmd(Make).execute([i, '-', name, path, '--mode=do-not-sync', '--nohl'])
            else:
                self.subcmd(Make).execute([i, '--', name, '--mode=do-not-sync', '--nohl'])

        self.subcmd(Make).execute(['all', '--', name, '--mode=only-sync', '--nohl'])


class Run(Endpoint):
    def name(self):
        return 'run'

    def _info(self):
        return ['{path} - запускает программу на удалённой машине']

    def _needHelp(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _rules(self):
        return [ Statement(['{path} рабочее_окружение -- путь_до_пограммы -- аргументы ',
                            '{space}путь_до_программы - относительный путь от корня рабочего окружения',
                            '{space}для показа справки надо вызвать {path} --help'], self.run,
                           lambda p: Rule(p).size().moreOrEquals(p.targets, 2)
                                            .size().moreOrEquals(p.delimers, 2)
                                            .size().equals(p.delimered[0], 1)
                                            .size().equals(p.delimered[1], 1)
                                            .check().delimersType(DoubleDelimer)) ]

    def _findSecondDelimer(self, args, index = 0):
        i = args.index(DoubleDelimer.value)
        return self._findSecondDelimer(args[i+1:], i+1) if index == 0 else i+index+1

    def run(self, p: Params):
        ws = self.database.selectone(p.delimered[0][0].value, Workspace)
        path = p.delimered[1][0].value

        i = self._findSecondDelimer(p.argv)

        for s in run(ws.host).withstderr().path(join(ws.path, path)).cmd(p.argv[i:]).exec():
            print(s, end='')


class Build(Command):
    def name(self) -> '':
        return 'build'

    def _info(self):
        return ['{path} - составные высокоуровневые команды для упрощения процесса разработки']

    def _commands(self) -> {}:
        return registerCommands(Deploy, Run)


commands = registerCommands(Build)
