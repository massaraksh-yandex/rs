from platform.params.params import Params
from platform.utils.utils import registerCommands, readLineWithPrompt
from platform.commands.command import Command
from platform.commands.endpoint import Endpoint
from platform.statement.statement import emptyCommand, singleOptionCommand
from src.utils.check import Exist, NotExist
from src.db.project import inputProject


class List(Endpoint):
    def name(self):
        return 'list'

    def _info(self):
        return ['{path} - показывает список проектов']

    def _rules(self):
        return emptyCommand(['{path}'], self.process)

    def process(self, p: Params):
        for k, v in self.database.projects().items():
            print("project: " + k)


class Show(Endpoint):
    def name(self):
        return 'show'

    def _info(self):
        return ['{path} - показывает информацию о проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        import src
        name = p.targets[0].value
        Exist(self.database).project(name)
        prj = self.database.selectone(name, src.db.project.Project)
        print(prj)


class Remove(Endpoint):
    def name(self):
        return 'rm'

    def _info(self):
        return ['{path} - удаляет запись о проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        import src
        name = p.targets[0].value
        Exist(self.database).project(name)
        answer = readLineWithPrompt('Удалить проект {0}? (yes/no)'.format(name), 'no')

        if answer != 'yes':
            print('Отмена...')
            return

        prj = self.database.selectone(name, src.db.project.Project)
        self.database.remove(prj)
        print('Проект {0} удалён'.format(name))


class Add(Endpoint):
    def name(self):
        return 'add'

    def _info(self):
        return ['{path} - создаёт запись о новом проекте']

    def _rules(self):
        return singleOptionCommand(['{path} название_проекта'], self.process)

    def process(self, p: Params):
        name = p.targets[0].value
        NotExist(self.database).project(name)
        prj = inputProject(name, self.database)
        if prj is not None:
            self.database.update(prj)
            print('Проект {0} добавлен'.format(prj.name))
        else:
            print('Отмена...')


class Project(Command):
    def name(self):
        return 'project'

    def _info(self):
        return ['{path} - команды управления проектами']

    def _commands(self):
        return registerCommands(Add, List, Remove, Show)


commands = registerCommands(Project)
