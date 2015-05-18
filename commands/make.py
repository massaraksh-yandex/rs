from collections import namedtuple
from platform.exception import WrongTargets
from platform.delimer import SingleDelimer, DoubleDelimer
from platform.utils import makeCommandDict
from platform.endpoint import Endpoint
from platform.params import Params
from src.config import Config
from src.workspace import Workspace, getWorkspaces
from src.project import getProjects
from commands.get import Get
from src.check_utils import Exist, Empty, NotEmpty, Check, Size, raiseWrongParsing
import subprocess
import sys


def make(make_targets, project, makefile_path = ''):
    def getRealWorkspacePath(ws: Workspace):
        sp = subprocess.Popen(['ssh', ws.host, 'cd {0} && readlink -m .'.format(ws.root)], stdout=subprocess.PIPE)
        return sp.stdout.readlines()[0].decode("utf-8").rstrip()

    prj = getProjects()[project]

    cd = 'cd {0}/{1}/{2}'.format(prj.path, project, makefile_path)
    jobs = 'CORENUM=$(cat /proc/cpuinfo | grep \"^processor\" | wc -l)'
    make = 'make {0} -j$CORENUM 2>&1'.format(' '.join(make_targets))

    command = "{0} && {1} && {2}".format(cd, jobs, make)

    ws = getWorkspaces()[prj.workspace]
    path = getRealWorkspacePath(ws)
    proc = subprocess.Popen(['ssh', ws.host, command], stdout=subprocess.PIPE)
    cfg = Config()
    while proc.poll() is None:
        line = proc.stdout.readline().decode("utf-8")
        line = line.replace(path, ws.root)
        line = line.replace('/home', cfg.homeFolderName)
        sys.stderr.write(line)


class Make(Endpoint):
    Args = namedtuple('Args', ['makeTargets', 'projects'])

    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'make'

    def _help(self):
        return ['{path} - вызывает Makefile на удалённой машине',
                '{path} цели -- названия_проектов',
                '{path} цели - название_проекта папка_с_Makefile']

    def _rules(self):
        singleMakefile = lambda p: self.makeMakefile if Size.equals(p.delimer, 1, 'Неверное число разделителей') and \
                                                        Check.delimerType(p.delimer[0], SingleDelimer) and \
                                                        Empty.options(p) and \
                                                        NotEmpty.array(self._parse(p).makeTargets) and \
                                                        Size.equals(self._parse(p).projects, 2) \
                                                     else raiseWrongParsing()

        manyProjects = lambda p: self.makeProjects if Size.equals(p.delimer, 1, 'Неверное число разделителей') and \
                                                      Check.delimerType(p.delimer[0], DoubleDelimer) and \
                                                      Empty.options(p) and \
                                                      NotEmpty.array(self._parse(p).makeTargets) and \
                                                      NotEmpty.array(self._parse(p).projects) \
                                                   else raiseWrongParsing()
        return [singleMakefile, manyProjects]

    def _parse(self, p: Params):
        ind = p.delimer[0].index
        if ind == 0:
            raise WrongTargets('Отсутствуют цели Makefile: ' + str(p.argv))
        if ind >= len(p.targets):
            raise WrongTargets('Отсутствуют проекты для сборки: ' + str(p.argv))

        return Make.Args(makeTargets=p.targets[:ind], projects=p.targets[ind:])

    def _syncIncludes(self, project):
        print('Синхронизирую заголовки...')
        pr = getProjects()[project]
        Get(self).execute([pr.workspace, '--workspace', '--path=include'])

    def makeProjects(self, p: Params):
        args = self._parse(p)
        for proj in args.projects:
            Exist.project(proj)
            print('Проект ' + proj)
            make(args.makeTargets, proj)
            self._syncIncludes(proj)

    def makeMakefile(self, p: Params):
        args = self._parse(p)
        Exist.project(args.projects[0])
        print('Проект ' + args.makeTargets[0]) # поправить вывод
        make(args.makeTargets, args.projects[0], args.projects[1])
        self._syncIncludes(args.projects[0])


module_commands = makeCommandDict([Make])
