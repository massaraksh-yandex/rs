from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.workspace import getWorkspaces
from src.sync import SyncData, callSync
from src.check_utils import Exist, Empty, NotEmpty, Check, Size, raiseWrongParsing
from os.path import expanduser


class Get(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'get'

    def _help(self):
        return ['{path} - получает файлы с удалённого сервера',
                '{path} --workspace [--path=src] окружение - получает часть рабочего окружения',
                '{space}Получает папку --path рабочего окружения',
                '{path} проект']

    def _rules(self):
        p = lambda p: self.syncProjects if Empty.delimers(p) and \
                                           Empty.options(p) and \
                                           NotEmpty.targets(p) \
                                        else raiseWrongParsing()

        w = lambda p: self.syncWorkspaces if Empty.delimers(p) and \
                                             NotEmpty.options(p) and \
                                             Check.optionNamesInSet(p, ['workspace', 'path']) and \
                                             Exist.option(p, 'workspace') and \
                                             Size.equals(p.targets, 1) \
                                          else raiseWrongParsing()
        return [p, w]

    def _syncPath(self, sd: SyncData):
        remote = '{0}:{1}/'.format(sd.host, sd.remotePath)
        callSync(sd.excludeFile, remote, expanduser(sd.path))

    def syncProjects(self, p: Params):
        for arg in p.targets:
            Exist.project(arg)
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self._syncPath(sd)

    def syncWorkspaces(self, p: Params):
        wsName = p.targets[0]
        Exist.workspace(wsName)
        ws = getWorkspaces()[wsName]
        path = ws.src
        if 'path' in p.options:
            path = getattr(ws, p.options['path'], ws.src)
        sd = ws.toSyncData(path)

        sd.showSyncInfo()
        self._syncPath(sd)


module_commands = makeCommandDict([Get])
