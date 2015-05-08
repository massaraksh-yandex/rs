import subprocess
import sys
from platform.exception import WrongTargets, WrongDelimers
from platform.params import Params
from platform.command import Endpoint
from platform.delimer import SingleDelimer
from platform.utils import makeCommandDict
from src.project import getProjects
from commands.get import Get
from src.workspace import getWorkspaceByHostAndPath


def make(make_targets, project, makefile_path = ''):
    def getRealWorkspacePath(proj):
        sp = subprocess.Popen(['ssh', prj.host, 'cd /home/massaraksh/ws; readlink -m .'], stdout=subprocess.PIPE)
        return sp.stdout.readlines()[0].decode("utf-8").rstrip()

    prj = getProjects()[project]

    cd = 'cd {0}/{1}/{2}'.format(prj.path, project, makefile_path)
    jobs = 'CORENUM=$(cat /proc/cpuinfo | grep \"^processor\" | wc -l)'
    make = 'make {0} -j$CORENUM 2>&1'.format(' '.join(make_targets))

    command = "{0}; {1}; {2}".format(cd, jobs, make)

    path = getRealWorkspacePath(prj)
    proc = subprocess.Popen(['ssh', prj.host, command], stdout=subprocess.PIPE)
    while proc.poll() is None:
        line = proc.stdout.readline().decode("utf-8")
        line = line.replace(path, '/Users/massaraksh/ws')
        line = line.replace('/home/massaraksh/', '/Users/massaraksh/')
        sys.stderr.write(line)

class Make(Endpoint):
    makeTargets = None
    projects = None

    def __init__(self, parent):
        super().__init__(parent)
        self.makeTargets = []
        self.projects = []

    def name(self):
        return 'make'

    def pathWithoutArgs(self):
        return 'rs make'

    def _help(self):
        return ['{path} - вызывает Makefile на удалённой машине',
                '{path} цели -- названия_проектов',
                '{path} цели - название_проекта папка_с_Makefile']

    def _check(self, p: Params):
        if len(p.delimer) != 1:
            raise WrongDelimers('Неверное число разделителей: ' + str(len(p.delimer)))

        delimer = p.delimer[0]
        ind = delimer.index

        if ind == 0:
            raise WrongTargets('Отсутствуют цели Makefile: ' + str(p.argv))
        if ind >= len(p.targets):
            raise WrongTargets('Отсутствуют проекты для сборки: ' + str(p.argv))

        self.makeTargets = p.targets[:ind]
        self.projects = p.targets[ind:]

        availableProjects = getProjects()
        if isinstance(delimer, SingleDelimer):
            if len(self.projects) != 2:
                raise WrongTargets('Слишком много параметров для сборки'
                                   ' проекта с указанием пути до Makefile: ' + str(self.projects))
            proj = self.projects[0]

            if proj not in availableProjects:
                raise WrongTargets('Нет такого проекта: ' + proj)
        else:
            for proj in self.projects:
                if proj not in availableProjects:
                    raise WrongTargets('Нет такого проекта: ' + proj)


    def syncIncludes(self, project):
        print('Синхронизирую заголовки...')
        pr = getProjects()[project]
        ws = getWorkspaceByHostAndPath(pr.host, pr.path)
        Get(self).execute([ws.name, '--workspace', '--includes-only'])

    def _process(self, p):
        delimer = p.delimer[0]
        if isinstance(delimer, SingleDelimer):
            print('Проект ' + self.makeTargets[0])
            make(self.makeTargets, self.projects[0], self.projects[1])
            self.syncIncludes(self.projects[0])
        else:
            for proj in self.projects:
                print('Проект ' + proj)
                make(self.makeTargets, proj)
                self.syncIncludes(proj)

module_commands = makeCommandDict([Make])

