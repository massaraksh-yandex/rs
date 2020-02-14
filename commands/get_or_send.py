from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import registerCommands
from src.db.project import Project
from src.sync.rsyncscp import RsyncSync, ArcSync
from src.sync.sync import Sync
from src.utils.check import Exist
from platform.statement.statement import Statement, Rule


class SendOrGet(object):
    def _rules_impl(self, h):
        return [Statement(['{path} [--dry] [--ws=имя] название_проекта',
                           '{space}--dry - показывает файлы, которые будут синхронизированы',
                           '{space}--ws - в какое рабочее окружение посылать проект',
                           '{space}--erase_missing - удаляет файлы, которых нет в папке назначения'], h,
                          lambda p: Rule(p).empty().delimers()
                                           .check().optionNamesInSet('dry', 'ws', 'erase_missing')
                                           .notEmpty().targets())]

    def _impl(self, p: Params):
        name = p.targets[0].value
        Exist(self.database).project(name)
        project: Project = self.database.projects()[name]

        if p.options['ws']:
            Exist(self.database).workspace(p.options['ws'])
            ws = self.database.workspaces()[p.options['ws']]
        else:
            ws = self.database.workspaces()[project.workspace]

        return Sync(database=self.database, obj=project, dry='dry' in p.options,
                    erase_missing='erase_missing' in p.options,
                    backend_class=ArcSync if ws.arc else RsyncSync, ws=ws).print()


class Send(SendOrGet, Endpoint):
    def name(self):
        return 'send'

    def _info(self):
        return ['{path} - отправляет файлы на удалённый сервер']

    def _rules(self):
        return self._rules_impl(self.send)

    def send(self, p: Params):
        self._impl(p).send()


class Get(SendOrGet, Endpoint):
    def name(self):
        return 'get'

    def _info(self):
        return ['{path} - получает файлы с удалённого сервера']

    def _rules(self):
        return self._rules_impl(self.get)

    def get(self, p: Params):
        self._impl(p).get()


commands = registerCommands(Send, Get)
