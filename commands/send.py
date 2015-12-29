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
        return [Statement(['{path} [--dry] [--workspace=имя] название_проекта',
                           '{space}--dry - показывает файлы, которые будут синхронизированы',
                           '{space}--workspace - в какое рабочее окружение посылать проект',
                           '{space}--erase_missing - удаляет файлы, которых нет в папке назначения'], self.send,
                          lambda p: Rule(p).empty().delimers()
                                           .check().optionNamesInSet('dry', 'workspace', 'erase_missing')
                                           .notEmpty().targets())]

    def send(self, p: Params):
        ws = p.options['workspace']
        if ws:
            Exist(self.database).workspace(ws)

        for arg in p.targets:
            name = arg.value
            Exist(self.database).project(name)
            project = self.database.projects()[name]
            project.workspace = ws or project.workspace
            Sync(self.database, project, 'dry' in p.options, 'erase_missing' in p.options).print().send()

commands = registerCommands(Send)
