import subprocess
from os.path import join

from platform.check import Check, NotEmpty, singleOptionCommand, raiseWrongParsing
from platform.delimer import SingleDelimer
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
        return [lambda p: self.run if Size.equals(p.targets, 2) and \
                                      Check.optionNamesInSet(p, 'workspace') and \
                                      NotEmpty.delimers(p) and \
                                      Check.delimerType(p.delimer[0], SingleDelimer) \
                                   else raiseWrongParsing()]

    def name(self) -> '':
        return 'run'

    def run(self, p: Params):
        Exist.project(p.targets[0])
        project = getProjects()[p.targets[0]]
        ws = getWorkspaces()[ p.options['workspace'] if 'workspace' in p.options else project.workspace ]
        internalPath = p.targets[1]
        name = join(ws.src, project.name, internalPath)
        command = 'cd "$(dirname {name})" && ./"$(basename {name})"'.format(name=name)
        subprocess.call(['ssh', ws.host, command])



class Build(Command):
    def name(self) -> '':
        return 'build'

    def _commands(self) -> {}:
        return makeCommandDict(Deploy, Run)


module_commands = makeCommandDict(Build)
