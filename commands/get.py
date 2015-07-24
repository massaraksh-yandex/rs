from os.path import expanduser

from platform.commands.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.workspace import getWorkspaces
from src.sync import SyncData, callSync
from src.check_utils import Exist
from platform.statement.statement import Rule, Statement


class Get(Endpoint):
    def name(self):
        return 'get'

    def _info(self):
        return ['{path} - получает файлы с удалённого сервера']

    def _rules(self):
        p = Statement(['{path} [--dry] проект',
                       '{space}--dry - показывает файлы, которые будут синхронизированы'], self.syncProjects,
                      lambda p: Rule(p).empty().delimers()
                                       .check().optionNamesInSet(['dry'])
                                       .notEmpty().targets())

        w = Statement(['{path} --workspace [--path=src] [--dry] окружение - получает часть рабочего окружения',
                       '{space}--path Получает указанную папку из рабочего окружения',
                       '{space}--dry - показывает файлы, которые будут синхронизированы'], self.syncWorkspaces,
                      lambda p: Rule(p).empty().delimers()
                                       .notEmpty().options()
                                       .check().optionNamesInSet(['workspace', 'path', 'dry'])
                                       .has().option('workspace')
                                       .size.equals(p.targets, 1))

        return [p, w]

    def _syncPath(self, sd: SyncData, p: Params):
        remote = '{0}:{1}/'.format(sd.host, sd.remotePath)
        callSync(sd.excludeFile, remote, expanduser(sd.path), 'dry' in p.options )

    def syncProjects(self, p: Params):
        for arg in p.targets:
            name = arg.value
            Exist.project(name)
            sd = getProjects()[name].toSyncData()
            sd.showSyncInfo()
            self._syncPath(sd, p)

    def syncWorkspaces(self, p: Params):
        wsName = p.targets[0].value
        Exist.workspace(wsName)
        ws = getWorkspaces()[wsName]
        path = ws.src
        if 'path' in p.options:
            path = getattr(ws, p.options['path'], ws.src)
        sd = ws.toSyncData(path)

        sd.showSyncInfo()
        self._syncPath(sd, p)


module_commands = makeCommandDict(Get)
