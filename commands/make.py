from platform.color.color import colored, Color, Style
from platform.params.delimer import SingleDelimer, DoubleDelimer
from platform.utils.utils import registerCommands
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from src.utils.maker import Maker
from commands.get import Get
from src.utils.check import Exist
from platform.statement.statement import Statement, Rule, InfoStatement


class Make(Endpoint):
    def name(self):
        return 'make'

    def _info(self):
        return ['{path} - вызывает Makefile на удалённой машине']

    def _rules(self):
        info = InfoStatement(['Опции:',
                              '{space}jobs - сколько потоков сборки запускать одновременно',
                              '{space}mode - регулирует что надо делать: собирать или синхронизировать папку include',
                              '{space}{space}all (или отсутсвие опции) - собирать и синхронизировать',
                              '{space}{space}do-not-sync - не синхронизировать include',
                              '{space}{space}only-sync - не собирать, только синхронизировать',
                              '{space}t - запускать ли тесты',
                              '{space}ws - окружение',
                              '{space}nohl - не окрашивать и не преобразовывать вывод'])

        sm = Statement(['{path} цели -- названия_проектов'], self.makeMakefile,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(SingleDelimer)
                                        .check().optionNamesInSet('jobs', 'mode', 'nohl', 't', 'ws')
                                        .check().optionValueInSet('mode', None, 'all', 'do-not-sync', 'only-sync')
                                        .notEmpty().array(p.delimered[0])
                                        .size().equals(p.delimered[1], 2))

        mp = Statement(['{path} цели - название_проекта папка_с_Makefile'], self.makeProjects,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(DoubleDelimer)
                                        .check().optionNamesInSet('jobs', 'mode', 'nohl', 't', 'ws')
                                        .check().optionValueInSet('mode', None, 'all', 'do-not-sync', 'only-sync')
                                        .notEmpty().array(p.delimered[0])
                                        .notEmpty().array(p.delimered[1]))

        return [info, sm, mp]

    def _make(self, p: Params, maker, name, path='.'):
        if p.options['mode'] != 'only-sync':
            path = (p.options['ws']+'/' if 'ws' in p.options else 'mail/') + name
            Exist(self.database).project(name)
            print()
            print(colored('Запуск сборки', Color.green, Style.underline))
            print('Проект: ' + colored(name, Color.blue))
            print('Цели: ' + colored(maker.maketargets, Color.blue))
            print('Путь: ' + colored(path, Color.blue))
            maker.make(name, path, need_highlight=not ('nohl' in p.options))

    def _syncIncludes(self, project, p: Params):
        if p.options['mode'] != 'do-not-sync':
            print()
            print(colored('Синхронизирую заголовки', Color.green, Style.underline))
            pr = self.database.projects()[project]
            self.subcmd(Get).execute([pr.workspace, '--workspace', '--path=include', '--erase_missing'])

    def makeProjects(self, p: Params):
        makeTargets = [x.value for x in p.delimered[0] if x.value.startswith('-')]
        maker = Maker(self.database, makeTargets, jobs=p.options['jobs'], tests=p.options['t'] if 't' in p.options else None)

        for name in [x.value for x in p.delimered[1]]:
            self._make(p, maker, name)
            self._syncIncludes(name, p)

    def makeMakefile(self, p: Params):
        makeTargets = [x.value for x in p.delimered[0]]

        targets = p.delimered[1]
        name = targets[0].value
        path = targets[1].value
        maker = Maker(self.database, makeTargets, jobs=p.options['jobs'], tests=p.options['t'] if 't' in p.options else None)

        self._make(p, maker, name, path)
        self._syncIncludes(name , p)


commands = registerCommands(Make)
