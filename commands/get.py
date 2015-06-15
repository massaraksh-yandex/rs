from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.workspace import getWorkspaces
from src.sync import SyncData, callSync
from src.check_utils import Exist
from platform.check import Size, Check, Empty, NotEmpty, Has, raiseWrongParsing
from os.path import expanduser


class Get(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)
        self.dry = 'dry'

    def name(self):
        return 'get'

    def _help(self):
        return ['{path} - получает файлы с удалённого сервера',
                '{path} --workspace [--path=src] [--dry] окружение - получает часть рабочего окружения',
                '{space}--path Получает указанную папку из рабочего окружения',
                '{path} [--dry] проект',
                '{space}--dry - показывает файлы, которые будут синхронизированы']

    def _rules(self):
        p = lambda p: self.syncProjects if Empty.delimers(p) and \
                                           Check.optionNamesInSet(p, [self.dry]) and \
                                           NotEmpty.targets(p) \
                                        else raiseWrongParsing()

        w = lambda p: self.syncWorkspaces if Empty.delimers(p) and \
                                             NotEmpty.options(p) and \
                                             Check.optionNamesInSet(p, ['workspace', 'path', self.dry]) and \
                                             Has.option(p, 'workspace') and \
                                             Size.equals(p.targets, 1) \
                                          else raiseWrongParsing()
        return [p, w]

    def _syncPath(self, sd: SyncData, p: Params):
        remote = '{0}:{1}/'.format(sd.host, sd.remotePath)
        callSync(sd.excludeFile, remote, expanduser(sd.path), self.dry in p.options )

    def syncProjects(self, p: Params):
        for arg in p.targets:
            Exist.project(arg)
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self._syncPath(sd, p)

    def syncWorkspaces(self, p: Params):
        wsName = p.targets[0]
        Exist.workspace(wsName)
        ws = getWorkspaces()[wsName]
        path = ws.src
        if 'path' in p.options:
            path = getattr(ws, p.options['path'], ws.src)
        sd = ws.toSyncData(path)

        sd.showSyncInfo()
        self._syncPath(sd, p)


module_commands = makeCommandDict(Get)
