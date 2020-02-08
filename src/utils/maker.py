import subprocess
import sys
from platform.color.color import Color, Style
from platform.color.highlighter import Highlighter, RR, CR
from platform.execute.run import run
from src.db.project import Project
from src.db.workspace import Workspace


class Maker(object):
    def __init__(self, database, targets, jobs=None, tests=None):
        self.maketargets = ' '.join(targets)
        self.jobs = '-j'+str(jobs) if jobs is not None else ''
        self.db = database
        self.cmd = ' && '.join(['cd {ws}/{makefilepath}',
                                f'~/arcadia/ya make {self.jobs}'+' {targets}'])
        if tests is not None:
            self.cmd += ' && ~/arcadia/ya make -{0} --keep-going'.format('t'*int(tests))

    def _getRealWorkspacePath(self, ws: Workspace):
        return run(ws.host).path(ws.path).cmd('readlink -m .').call().rstrip()

    def _getHighlighter(self, ws: Workspace, prj: Project):
        path = self._getRealWorkspacePath(ws)

        return Highlighter(RR(path, ws.path, Color.no), RR('/home', self.db.config.homeFolderName, Color.no),
                           RR(r'\[with', '\n[\n with'), RR(r'\;', ';\n'),
                           CR(r'^[\/~][^:\ ]+', Color.cyan, Style.underline), CR(r'\serror\:', Color.red, Style.bold),
                           CR(r'\sОшибка', Color.red, Style.bold), CR(r'\swarning\:', Color.yellow),
                           RR(r',', ',', Color.green), RR(r'<', '<', Color.green),
                           RR(r'>', '>', Color.green), CR(r'\[\s*\d+%\]', Color.violent),
                           CR(r'[0-9]+ - GOOD', Color.green), CR(r'[0-9]+ - FAIL', Color.red), CR(r'-------', Color.blue),
                           CR(r'WARN', Color.yellow), CR(r'DEBUG', Color.yellow),
                           CR(r'INFO', Color.blue), CR(r'WARN', Color.violent), CR(r'ERROR', Color.red),
                           CR(r'Failed', Color.red),
                           CR(r'\[TS\]', Color.green),
                           RR(r'~/rtc', '~/go/src/a.yandex-team.ru', Color.no)
                           )

    def _getNameReplaces(self, ws: Workspace, prj: Project):
        path = self._getRealWorkspacePath(ws)
        return Highlighter(RR(path, ws.path, Color.no), RR('/home', self.db.config.homeFolderName, Color.no))

    def make(self, name, path='.', need_highlight=True):
        project = self.db.selectone(name, Project)
        ws = self.db.selectone(project.workspace, Workspace)
        hl = (self._getHighlighter if need_highlight else self._getNameReplaces)(ws, project)

        self.cmd = self.cmd.format(ws=ws.src, prj=name, makefilepath=path, targets=self.maketargets, jobs=self.jobs)

        print(str(self.cmd))

        p = run(ws.host).withstderr().cmd(self.cmd)
        for s in p.exec():
            sys.stderr.write(hl.highlight(s))
            sys.stderr.flush()
