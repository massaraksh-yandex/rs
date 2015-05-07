from platform.exception import WrongTargets, WrongOptions
from platform.command import Command
from platform.delimer import checkNoDelimers
from platform.utils import makeCommandDict
from src.settings import Settings
from src.project import getProjects
from src.workspace import getWorkspaces
from src.sync import SyncData, callSync


class Get(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'get'

    def __help(self):
        print('rs get - получает файлы с удалённого сервера')
        print('rs get название_проекта')
        print('rs get --help')

    def __check(self, p):
        checkNoDelimers(p)
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            for opt in p.options:
                if opt not in ['workspace', 'includes-only']:
                    raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, sd: SyncData):
        remote = '{0}:{1}/'.format(sd.host, sd.remotePath)
        callSync([Settings.RS_ARGS, '--cvs-exclude', sd.excludeFile, remote, sd.path])

    def syncProjects(self, p):
        for arg in p.targets:
            sd = getProjects()[arg].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd)

    def syncWorkspaces(self, p):
        for arg in p.targets:
            ws = getWorkspaces()[arg]
            sd = ws.toSyncData(ws.include if 'includes-only' in p.options else ws.src)

            sd.showSyncInfo()
            self.syncPath(sd)

    def __process(self, p):
        try:
            if 'workspace' in p.options:
                self.syncWorkspaces(p)
            else:
                self.syncProjects(p)
        except KeyError as arg:
            self.error('Нет такого проекта: ' + str(arg))


module_commands = makeCommandDict([Get])
