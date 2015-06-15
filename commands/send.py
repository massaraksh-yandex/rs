from os.path import expanduser
from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.sync import SyncData, callSync
from src.check_utils import Exist
from platform.check import Check, Empty, NotEmpty, raiseWrongParsing


class Send(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)
        self.dry = 'dry'

    def name(self):
        return 'send'

    def _help(self):
        return ['{path} - отправляет файлы на удалённый сервер',
                '{path} [--dry] название_проекта',
                '{space}--dry - показывает файлы, которые будут синхронизированы']

    def syncPath(self, sd: SyncData, p : Params):
        remote = '{0}:{1}'.format(sd.host, sd.path)
        callSync(sd.excludeFile, expanduser(sd.path)+'/', remote, self.dry in p.options)

    def _rules(self):
        p = lambda p: self.send if Empty.delimers(p) and \
                                   Check.optionNamesInSet(p, [self.dry]) and \
                                   NotEmpty.targets(p) \
                                else raiseWrongParsing()

        return [p]

    def send(self, p: Params):
        for arg in p.targets:
            Exist.project(arg)
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd, p)


module_commands = makeCommandDict(Send)
