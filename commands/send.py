from os.path import expanduser
from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.sync import SyncData, callSync
from src.check_utils import Exist, singleOptionCommand


class Send(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'send'

    def _help(self):
        return ['{path} - отправляет файлы на удалённый сервер',
                '{path} название_проекта']

    def syncPath(self, sd: SyncData):
        remote = '{0}:{1}'.format(sd.host, sd.path)
        callSync(sd.excludeFile, expanduser(sd.path)+'/', remote)

    def _rules(self):
        return singleOptionCommand(self.send)

    def send(self, p: Params):
        for arg in p.targets:
            Exist.project(arg)
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd)


module_commands = makeCommandDict([Send])
