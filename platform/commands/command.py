from abc import abstractmethod
from platform.commands.basecommand import BaseCommand
from platform.params.params import Params
from platform.params.exception import PlatformException
from platform.statement.statement import Statement, Rule


class Command(BaseCommand):
    def _needHelp(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _rules(self) -> []:
        ret = []
        for k, v in self._commands().items():
            cmd = v(self, self.database)
            ret.append(Statement([ cmd._listToMessage(cmd._info()) ], True,
                                 lambda p, name=k: Rule(p).notEmpty().targets().check().target(0, name)))

        return ret

    def _process(self, p: Params, res):
        self.subcmd(self._commands()[p.argv[0]]).execute(p.argv[1:])

    def _ignoredexceptions(self) -> ():
        return (PlatformException, KeyError)

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _commands(self) -> {}:
        pass

