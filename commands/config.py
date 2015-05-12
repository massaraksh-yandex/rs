from platform.delimer import checkNoDelimers
from platform.command import Endpoint
from platform.exception import WrongOptions, WrongTargets
from platform.params import Params
from platform.utils import makeCommandDict
from src import config
from src.check_utils import Exist, Empty, Size, raiseWrongParsing


class Config(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'config'

    def _help(self):
        return ['{path} - настройки опций программы',
                '{path} --list - показывает текущие опции',
                '{path} опция - печатает значение опции',
                '{path} опция новое_значение - устанавливает новое значение для опции']

    def _checkNew(self):
        a = lambda p: self.showOptions if Empty.delimers(p) and \
                                          Empty.targets(p) and \
                                          Exist.option(p, 'list') \
                                       else raiseWrongParsing()

        b = lambda p: self.showOption if Empty.delimers(p) and \
                                         Size.equals(p.targets, 1) and \
                                         Empty.options(p) \
                                      else raiseWrongParsing()

        c = lambda p: self.setOption if Empty.delimers(p) and \
                                        Size.equals(p.targets, 2) and \
                                        Empty.options(p) \
                                     else raiseWrongParsing()

        return [a, b, c]

    def showOptions(self, p: Params):
        config.Config().print()

    def showOption(self, p: Params):
        print(getattr(config.Config(), p.targets[0]))

    def setOption(self, p: Params):
        cfg = config.Config()
        setattr(cfg, p.targets[0], p.targets[1])
        cfg.serialize()

    def _check(self, p: Params):
        checkNoDelimers(p)

        lopt = len(p.options)
        ltar = len(p.targets)

        if lopt == 0 and ltar > 2:
            raise WrongTargets('Неверное чило аргументов: ' + str(p.targets))
        elif lopt == 1 and ltar > 0:
            raise WrongTargets('Неверное чило аргументов: ' + str(p.targets))
        elif lopt > 1:
            raise WrongOptions('Странные опции: ' + str(p.options))

    def _process(self, p: Params):
        l = len(p.targets)

        cfg = config.Config()
        if l == 0:
            cfg.print()
        elif l == 1:
            print(getattr(cfg, p.targets[0]))
        else:
            setattr(cfg, p.targets[0], p.targets[1])
            cfg.serialize()

module_commands = makeCommandDict([Config])