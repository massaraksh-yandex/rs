from platform.params.delimer import SingleDelimer, DoubleDelimer
from platform.utils.utils import makeCommandDict
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from src.maker import Maker
from commands.get import Get
from src.check import Exist
from platform.statement.statement import Statement, Rule


class Make(Endpoint):
    def name(self):
        return 'make'

    def _info(self):
        return ['{path} - вызывает Makefile на удалённой машине']

    def _rules(self):

        sm = Statement(['{path} цели -- названия_проектов'], self.makeMakefile,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(SingleDelimer)
                                        .check().optionNamesInSet('jobs')
                                        .notEmpty().array(p.delimered[0])
                                        .size().equals(p.delimered[1], 2))

        mp = Statement(['{path} цели - название_проекта папка_с_Makefile'], self.makeProjects,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(DoubleDelimer)
                                        .check().optionNamesInSet('jobs')
                                        .notEmpty().array(p.delimered[0])
                                        .notEmpty().array(p.delimered[1]))

        return [sm, mp]

    def _syncIncludes(self, project):
        print('Синхронизирую заголовки...')
        pr = self.database.projects()[project]
        self.subcmd(Get).execute([pr.workspace, '--workspace', '--path=include'])

    def makeProjects(self, p: Params):
        makeTargets = [ x.value for x in p.delimered[0] ]
        maker = Maker(self.database, makeTargets, p.options['jobs'])

        for name in [ x.value for x in p.delimered[1] ]:
            Exist(self.database).project(name)
            print('Проект ' + name)
            maker.make(name)
            self._syncIncludes(name)

    def makeMakefile(self, p: Params):
        makeTargets = p.delimered[0]
        targets = p.delimered[1]
        name = targets.projects[0].value

        Exist(self.database).project(name)
        print('Проект ' + name)

        Maker(self.database, makeTargets, p.options['jobs']).make(name, targets[1].name)
        self._syncIncludes(name)


module_commands = makeCommandDict(Make)
