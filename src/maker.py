import subprocess
import sys
from platform.color.color import Color, Style
from platform.color.highlighter import Highlighter, RR, CR
from src.project import Project
from src.workspace import Workspace


class Maker(object):
    def __init__(self, database, makeTargets, jobs = None):
        self.maketargets = ' '.join(makeTargets)
        self.jobs = jobs or '$(cat /proc/cpuinfo | grep \"^processor\" | wc -l)'
        self.db = database
        self.cmd = ' && '.join(['cd {ws}/{prj}/{makefilepath}',
                                'CORENUM={jobs}',
                                'make {targets} -j$CORENUM 2>&1'])

    def _getRealWorkspacePath(self, ws: Workspace):
        sp = subprocess.Popen(['ssh', ws.host, 'cd {0} && readlink -m .'.format(ws.path)], stdout=subprocess.PIPE)
        return sp.stdout.readlines()[0].decode('utf-8').rstrip()

    def _getHighlighter(self, ws: Workspace, prj: Project):
        path = self._getRealWorkspacePath(ws)

        return Highlighter(RR(path, ws.path, Color.no), RR('/home', self.db.config.homeFolderName, Color.no),
                           RR(r'\[with', '\n[\n with'), RR(r'\;', ';\n'),
                           CR(r'^[\/~][^\:]*', Color.cyan, Style.underline), CR(r'\serror\:', Color.red, Style.bold),
                           CR(r'\sОшибка', Color.red, Style.bold), CR(r'\swarning\:', Color.yellow),
                           RR(r',', ',', Color.green), RR(r'<', '<', Color.green),
                           RR(r'>', '>', Color.green), CR(r'\[\s*\d+%\]', Color.violent))

    def make(self, name, path = '.'):
        project = self.db.selectone(name, Project)
        ws = self.db.selectone(project.workspace, Workspace)
        hl = self._getHighlighter(ws, project)

        self.cmd = self.cmd.format(ws=ws.src, prj=name, makefilepath=path, targets=self.maketargets, jobs=self.jobs)

        proc = subprocess.Popen(['ssh', ws.host, self.cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if line == '':
                break
            line = hl.highlight(line)
            sys.stderr.write(line)
            sys.stderr.flush()