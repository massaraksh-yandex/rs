from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import registerCommands
from src.sync.sync import Sync
from src.utils.check import Exist
from platform.statement.statement import Rule, Statement
from src.db.workspace import Workspace


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
                                       .size().equals(p.targets, 1))

        return [p, w]

    def syncProjects(self, p: Params):
        projects = self.database.projects()
        for arg in p.targets:
            name = arg.value
            Exist(self.database).project(name)
            project = projects[name]
            Sync(self.database, project, dry='dry' in p.options).print().get()

    def syncWorkspaces(self, p: Params):
        wsName = p.targets[0].value
        Exist(self.database).workspace(wsName)
        ws = self.database.selectone(wsName, Workspace)

        ws.src = ws.path
        if 'path' in p.options:
            ws.name = p.options['path']

        Sync(self.database, ws, dry='dry' in p.options).print().get()


commands = registerCommands(Get)
