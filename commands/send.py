from platform.exception import WrongOptions, WrongTargets
from platform.delimer import checkNoDelimers
from platform.command import Command
from platform.utils import makeCommandDict
from src.settings import Settings
from src.project import getProjects
from src.sync import SyncData, callSync


class Send(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'send'

    def help(self):
        print('rs send - отправляет файлы на удалённый сервер')
        print('rs send название_проекта')
        print('rs send --help')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, sd: SyncData):
        remote = '{0}:{1}'.format(sd.host, sd.path)
        callSync([Settings.RS_ARGS, '--cvs-exclude', sd.excludeFile, sd.path+'/', remote])


    def process(self, p):
        try:
            for arg in p.targets:
                sd = getProjects()[arg].toSyncData()
                sd.showSyncInfo()
                self.syncPath(sd)
        except KeyError:
            self.error('Нет такого проекта: ' + arg)


module_commands = makeCommandDict([Send])
