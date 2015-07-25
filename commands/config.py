from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import makeCommandDict
from src import config
from platform.statement.statement import Statement, Rule


class Config(Endpoint):
    def name(self):
        return 'config'

    def _info(self):
        return ['{path} - настройки опций программы']

    def _rules(self):
        a = Statement(['{path} --list - показывает текущие опции'], self.showOptions,
                      lambda p: Rule(p).empty().delimers()
                                       .empty().targets()
                                       .has().option('list'))

        b = Statement(['{path} --init - возвращает конфигурационный файл к начальному состоянию'], self.initConfig,
                      lambda p: Rule(p).empty().delimers()
                                       .empty().targets()
                                       .has().option('init'))

        c = Statement(['{path} опция - печатает значение опции'], self.showOption,
                      lambda p: Rule(p).empty().delimers()
                                       .size().equals(p.targets, 1)
                                       .empty().options())

        d = Statement(['{path} опция значение - устанавливает новое значение для опции',
                       '{path} опция значение1,значение2 - устанавливает значение опции-массива'], self.setOption,
                      lambda p: Rule(p).empty().delimers()
                                       .size().equals(p.targets, 2)
                                       .empty().options())

        return [a, b, c, d]

    def showOptions(self, p: Params):
        print(self.config)

    def showOption(self, p: Params):
        print(getattr(self.config, p.targets[0].value))

    def setOption(self, p: Params):
        cfg = self.config
        attr = p.targets[0].value
        value = p.targets[1].value
        if isinstance(getattr(cfg, attr), list):
            setattr(cfg, attr, value.split(','))
        else:
            cfg._replace()
            setattr(cfg, attr, value)
        cfg.serialize()

    def initConfig(self, p: Params):
        config.Config.defaultConfig().serialize()


module_commands = makeCommandDict(Config)