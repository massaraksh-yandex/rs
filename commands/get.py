from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from platform.utils.utils import makeCommandDict
from src.sync import Sync
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
                                       .size().equals(p.targets, 1))

        return [p, w]

    def syncProjects(self, p: Params):
        for arg in p.targets:
            name = arg.value
            Exist(self.database).project(name)
            project = self.database.projects()[name]
            Sync(self.database, self.config, project, dry='dry' in p.options).print().get()

    def syncWorkspaces(self, p: Params):
        wsName = p.targets[0].value
        Exist(self.database).workspace(wsName)
        ws = self.database.workspaces()[wsName]
        if 'path' in p.options:
            ws.name = p.options['path']
        ws.src = ws.path
        Sync(self.database, self.config, ws, dry='dry' in p.options).print().get()


module_commands = makeCommandDict(Get)
