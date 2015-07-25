from os.path import expanduser
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import makeCommandDict
from src.project import getProjects
from src.sync import SyncData, callSync
from src.check_utils import Exist
from platform.statement.statement import Statement, Rule


class Send(Endpoint):
    def name(self):
        return 'send'

    def _info(self):
        return ['{path} - отправляет файлы на удалённый сервер']

    def _rules(self):
        p = Statement(['{path} [--dry] название_проекта',
                       '{space}--dry - показывает файлы, которые будут синхронизированы'], self.send,
                      lambda p: Rule(p).empty().delimers()
                                       .check().optionNamesInSet(['dry'])
                                       .notEmpty().targets())

        return [ p ]

    def syncPath(self, sd: SyncData, p : Params):
        remote = '{0}:{1}'.format(sd.host, sd.remotePath)
        callSync(sd.excludeFile, expanduser(sd.path)+'/', remote, 'dry' in p.options)

    def send(self, p: Params):
        for arg in p.targets:
            name = arg.value
            Exist.project(name)
            sd = getProjects()[name].toSyncData()
            sd.showSyncInfo()
            self.syncPath(sd, p)


module_commands = makeCommandDict(Send)
