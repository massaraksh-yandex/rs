from platform.delimer import checkNoDelimers
from platform.command import Endpoint
from platform.exception import WrongOptions, WrongTargets
from platform.params import Params
from platform.utils import makeCommandDict
from src import config


class Config(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'config'

    def _help(self):
        return ['{path} - настройки опций программы',
                '{path} - показывает текущие опции',
                '{path} опция - печатает значение опции',
                '{path} опция новое_значение - устанавливает новое значение для опции']

    def _check(self, p: Params):
        checkNoDelimers(p)

        if len(p.targets) > 2:
            raise WrongTargets('Неверное чило аргументов: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

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