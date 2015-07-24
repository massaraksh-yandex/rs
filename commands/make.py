import subprocess
import sys

from platform.color.color import Color, Style
from platform.color.highlighter import Highlighter, RR, CR
from platform.params.delimer import SingleDelimer, DoubleDelimer
from platform.utils.utils import makeCommandDict
from platform.commands.endpoint import Endpoint
from platform.params.params import Params
from src.config import Config
from src.workspace import Workspace, getWorkspaces
from src.project import getProjects
from commands.get import Get
from src.check_utils import Exist
from platform.statement.statement import Statement, Rule

hl = Highlighter(RR(r"\[with", '\n[\n with'), RR(r"\;", ';\n'),
                 CR(r"^[\/~][^\:]*", Color.cyan, Style.underline), CR(r"\serror\:", Color.red, Style.bold),
                 CR(r"\sОшибка", Color.red, Style.bold), CR(r"\swarning\:", Color.yellow),
                 RR(r",", ',', Color.green), RR(r"<", '<', Color.green),
                 RR(r">", '>', Color.green), CR(r"\[\s*\d+%\]", Color.violent))


def make(make_targets, project, makefile_path = '', jobs = None):
    def getRealWorkspacePath(ws: Workspace):
        sp = subprocess.Popen(['ssh', ws.host, 'cd {0} && readlink -m .'.format(ws.root)], stdout=subprocess.PIPE)
        return sp.stdout.readlines()[0].decode("utf-8").rstrip()

    prj = getProjects()[project]
    ws = getWorkspaces()[prj.workspace]

    cd = 'cd {0}/{1}/{2}'.format(ws.src, project, makefile_path)
    jobs = 'CORENUM=' + (jobs or '$(cat /proc/cpuinfo | grep \"^processor\" | wc -l)')
    make = 'make {0} -j$CORENUM 2>&1'.format(' '.join(make_targets))

    command = "{0} && {1} && {2}".format(cd, jobs, make)

    path = getRealWorkspacePath(ws)
    cfg = Config.instance
    proc = subprocess.Popen(['ssh', ws.host, command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    while True:
        line = proc.stdout.readline().decode("utf-8")
        if line == '':
            break

        line = line.replace(path, prj.path)
        line = line.replace('src/src/', 'src/')
        line = line.replace('/ht/', '/ws/')
        line = line.replace('/home', cfg.homeFolderName)
        line = hl.highlight(line)
        sys.stderr.write(line)
        sys.stderr.flush()


class Make(Endpoint):
    def name(self):
        return 'make'

    def _info(self):
        return ['{path} - вызывает Makefile на удалённой машине']

    def _rules(self):

        sm = Statement(['{path} цели -- названия_проектов'], self.makeMakefile,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(SingleDelimer)
                                        .check().optionNamesInSet('jobs')
                                        .notEmpty().array(p.delimered[0])
                                        .size().equals(p.delimered[1], 2))

        mp = Statement(['{path} цели - название_проекта папка_с_Makefile'], self.makeProjects,
                       lambda p: Rule(p).size().equals(p.delimers, 1)
                                        .check().delimersType(DoubleDelimer)
                                        .check().optionNamesInSet('jobs')
                                        .notEmpty().array(p.delimered[0])
                                        .notEmpty().equals(p.delimered[1]))

        return [sm, mp]

    def _syncIncludes(self, project):
        print('Синхронизирую заголовки...')
        pr = getProjects()[project]
        Get(self).execute([pr.workspace, '--workspace', '--path=include'])

    def makeProjects(self, p: Params):
        makeTargets = [ x.value for x in p.delimered[0] ]
        projects = p.delimered[1]
        for proj in projects:
            name = proj.value
            Exist.project(name)
            print('Проект ' + name)
            make(makeTargets, name, jobs=p.options['jobs'])
            self._syncIncludes(name)

    def makeMakefile(self, p: Params):
        makeTargets = p.delimered[0]
        targets = p.delimered[1]

        name = targets.projects[0].value
        Exist.project(name)
        print('Проект ' + name)
        make(makeTargets, name, targets[1].name, jobs=p.options['jobs'])
        self._syncIncludes(name)


module_commands = makeCommandDict(Make)
