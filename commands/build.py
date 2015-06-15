import subprocess
from os.path import join

from platform.check import singleOptionCommand, raiseWrongParsing
from platform.endpoint import Endpoint
from platform.command import Command
from platform.utils import makeCommandDict
from src.check_utils import *
from commands.send import Send
from commands.make import Make


class Deploy(Endpoint):
    def _help(self) -> []:
        return ['{path} - отсылает проект на сервер и компилирует его',
                '{path} проект',
                '{space}Для синхронизации используется команда send проект',
                '{space}Для построения make all install -- проект']

    def _rules(self) -> []:
        return singleOptionCommand(self.deploy)

    def name(self) -> '':
        return 'deploy'

    def deploy(self, p: Params):
        name = p.targets[0]
        Exist.project(name)
        Send(self).execute([name])
        Make(self).execute(['all', 'install', '--', name])
        Make(self).execute(['check', '--', name])


class Run(Endpoint):
    def _help(self) -> []:
        return ['{path} - запускает программу на удалённой машине',
                '{path} проект [--workspace] - путь_до_программы',
                '{space}путь_до_программы берётся относительно корневой папки проекта',
                '{space}--workspace - если параметр не указан, то берётся станрадтное рабочее окружение проекта']

    def _rules(self) -> []:
        return [lambda p: self.run]

    def name(self) -> '':
        return 'run'

    def _makeParams(self, argv):
        p = Params.makeRawParams(argv)
        if len(argv) == 0:
            p._helpOptionIndex = 0
        return p

    def parseArgs(self, p: Params):
        projectName = None
        workspace = None
        args = []

        sep = p.argv.index('-')
        if sep == 1:
            projectName = p.argv[0]
        elif sep == 2:
            projectName = p.argv[0]
            k, workspace = Params.parseOption(p.argv[1])
            if k != 'workspace' or not workspace:
                raiseWrongParsing()
        else:
            raiseWrongParsing()

        pathToProgram = p.argv[sep+1]

        if len(p.argv) > sep+2:
            if p.argv[sep+2] != '-':
                raiseWrongParsing()
            args = p.argv[sep+3:]

        Exist.project(projectName)
        project = getProjects()[projectName]
        ws = getWorkspaces()[ workspace if workspace else project.workspace ]

        return (project, ws, pathToProgram, args)

    def run(self, p: Params):
        project, ws, pathToProgram, args = self.parseArgs(p)
        name = join(ws.src, project.name, pathToProgram)
        command = 'cd "$(dirname {name})" && ./"$(basename {name})" {args}'.format(name=name, args=' '.join(args))
        subprocess.call(['ssh', ws.host, command])



class Build(Command):
    def name(self) -> '':
        return 'build'

    def _commands(self) -> {}:
        return makeCommandDict(Deploy, Run)


module_commands = makeCommandDict(Build)
