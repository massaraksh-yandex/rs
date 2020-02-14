from platform.color.color import colored, Color, Style
from platform.utils.utils import registerCommands
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from src.db.project import Project
from src.db.workspace import Workspace
from src.utils.maker import Maker
from src.utils.check import Exist
from platform.statement.statement import Statement, Rule, InfoStatement


class Make(Endpoint):
    def name(self):
        return 'make'

    def _info(self):
        return ['{path} - вызывает ya make на удалённой машине']

    def _rules(self):
        info = InfoStatement(['Опции:',
                              '{space}t - small',
                              '{space}tt - medium',
                              '{space}ttt - large',
                              '{space}ws - окружение',
                              '{space}add_tests - доп тесты',
                              '{space}add_builds - доп сборки',
                              '{space}nohl - не окрашивать и не преобразовывать вывод'])

        sm = Statement(['{path} название проектов'], self.make,
                       lambda p: Rule(p).size().equals(p.targets, 1)
                                        .check().optionNamesInSet('nohl', 't', 'tt', 'ttt', 'ws',
                                                                  'add_tests', 'add_builds'))

        return [info, sm]

    def make(self, p: Params):
        name = p.targets[0].value
        maker = Maker(self.database)

        Exist(self.database).project(name)
        project: Project = self.database.selectone(name, Project)

        ws_name = p.options['ws'] if 'ws' in p.options else project.workspace
        Exist(self.database).workspace(ws_name)
        ws: Workspace = self.database.selectone(ws_name, Workspace)

        print()
        print(colored('Запуск сборки', Color.green, Style.underline))
        print('Проект: ' + colored(name, Color.blue))
        print('Путь: ' + colored(project.path, Color.blue))
        print('Инфо: ' + colored(project.__dict__, Color.blue))
        print('Workspace: ' + colored(ws.__dict__, Color.blue))

        test_level = None
        test_level = 't' if 't' in p.options else test_level
        test_level = 'tt' if 'tt' in p.options else test_level
        test_level = 'ttt' if 'ttt' in p.options else test_level

        maker.make(project=project, ws=ws, test_level=test_level, add_tests='add_tests' in p.options,
                   add_build='add_builds' in p.options, need_highlight=not ('nohl' in p.options))


commands = registerCommands(Make)
