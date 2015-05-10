from platform.exception import WrongOptions, WrongTargets
from platform.delimer import checkNoDelimers
from platform.command import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.sync import SyncData, callSync


class Send(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'send'

    def _help(self):
        return ['{path} - отправляет файлы на удалённый сервер',
                '{path} название_проекта']

    def _check(self, p: Params):
        checkNoDelimers(p)
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        projects = getProjects()
        for arg in p.targets:
            if arg not in projects:
                raise WrongTargets('Нет такого проекта: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, sd: SyncData):
        remote = '{0}:{1}'.format(sd.host, sd.path)
        callSync(sd.excludeFile, sd.path+'/', remote)


    def _process(self, p: Params):
        for arg in p.targets:
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd)


module_commands = makeCommandDict([Send])
