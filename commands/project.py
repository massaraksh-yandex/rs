from os import path
from src.projects_repo import getProjects
from platform.exception import WrongOptions, WrongTargets
from platform.command import Command


def findAllImpl(path, regexp, direcroty):
    return []


def findAllFiles(path, regexp):
    return findAllImpl(path, regexp, False)


def findAllDirs(path, regexp):
    return findAllImpl(path, regexp, True)


def findAll(path, finder, types):
    ret = []
    for t in types:
        finder(path, t)
    return ret


def createQtcreatorImportProject(name, full_path):
    def createFilesFile(name, path, content):
        pass

    def createIncludesFile(name, path, content):
        pass

    def createConfigFile(name, path):
        pass  # empty

    def createCreatorFile(name, path):
        pass  # just [General]

    files = findAll(path, findAllFiles, ['*.cpp', '*.cxx', '*.cc', '*.c',
                                         '*.hpp', '*.hxx', '*.hh', '*.h'])

    direcroties = findAll(path, findAllDirs, ['*'])

    createFilesFile(name, path, files)
    createIncludesFile(name, path, direcroties)
    createConfigFile(name, path)
    createCreatorFile(name, path)


def createQmakeProject(name, full_path):
    def createProjectFile(name, path, sources, headers, dirs):
        pass  # TEMPLATE = aux

    sources = findAll(path, findAllFiles, ['*.cpp', '*.cxx', '*.cc', '*.c'])
    headers = findAll(path, findAllFiles, ['*.hpp', '*.hxx', '*.hh', '*.h'])
    direcroties = findAll(path, findAllDirs, ['*'])

    createProjectFile(name, path, sources, headers, direcroties)


class List(Command):
    def help(self):
        print('list - показывает список проектов')
        print('rs project list [--help]')

    def check(self, p):
        if len(p.targets) != 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def process(self, p):
        for k, v in getProjects().items():
            print("project: " + k)


class Create(Command):
    def projectPath(self, name):
        return '/home/massaraksh/ws/src'

    def help(self):
        print('create проект - создаёт запись о новом проекте')
        print('rs project create [проект]')
        print('rs project create --help')
        print('[проект] - название проекта')

    def check(self, p):
        if len(p.targets) != 1:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))
        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def process(self, p):
        name = p.targets[0]
        # with open(join(Settings.REMOTES_DIR, name+'.py'), 'w') as f:
        str = "\"path\":\"{0}\", \"host\": \"{1}\", \"type\":\"{2}\"".format(self.projectPath(name), 'wmidevaddr',
                                                                             'qtcreator_import')
        # f.write("data = {" + str + " } ")
        print(str)

class Project(Command):
    commands = {'create': Create, 'list': List}

    def help(self):
        print('rs project create')
        print('rs project list')

    def check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('')


    def process(self, p):
        cmd = p.targets[0]
        v = self.commands[cmd]()
        v.execute(p.argv[1:])


module_commands = {'project': Project}
