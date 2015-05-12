from platform.exception import WrongTargets, WrongOptions
from platform.command import Endpoint
from platform.delimer import checkNoDelimers
from platform.params import Params
from platform.utils import makeCommandDict
from src.project import getProjects
from src.workspace import getWorkspaces
from src.sync import SyncData, callSync
from os.path import expanduser


class Get(Endpoint):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'get'

    def _help(self):
        return ['{path} - получает файлы с удалённого сервера',
                '{path} название_проекта']

    def _check(self, p: Params):
        checkNoDelimers(p)
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            for opt in p.options:
                if opt not in ['workspace', 'includes-only']:
                    raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, sd: SyncData):
        remote = '{0}:{1}/'.format(sd.host, sd.remotePath)
        callSync(sd.excludeFile, remote, expanduser(sd.path))

    def syncProjects(self, p: Params):
        for arg in p.targets:
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd)

    def syncWorkspaces(self, p: Params):
        for arg in p.targets:
            ws = getWorkspaces()[arg]
            sd = ws.toSyncData(ws.include if 'includes-only' in p.options else ws.src)

            sd.showSyncInfo()
            self.syncPath(sd)

    def _process(self, p: Params):
        try:
            if 'workspace' in p.options:
                self.syncWorkspaces(p)
            else:
                self.syncProjects(p)
        except KeyError as arg:
            self._error('Нет такого проекта: ' + str(arg))


module_commands = makeCommandDict([Get])
