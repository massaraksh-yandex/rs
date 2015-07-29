from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import registerCommands
from src.sync.sync import Sync
from src.utils.check import Exist
from platform.statement.statement import Statement, Rule


class Send(Endpoint):
    def name(self):
        return 'send'

    def _info(self):
        return ['{path} - отправляет файлы на удалённый сервер']

    def _rules(self):
        return [Statement(['{path} [--dry] название_проекта',
                           '{space}--dry - показывает файлы, которые будут синхронизированы'], self.send,
                          lambda p: Rule(p).empty().delimers()
                                           .check().optionNamesInSet(['dry'])
                                           .notEmpty().targets())]

    def send(self, p: Params):
        for arg in p.targets:
            name = arg.value
            Exist(self.database).project(name)
            project = self.database.projects()[name]
            Sync(self.database, project, dry='dry' in p.options).print().send()

commands = registerCommands(Send)
