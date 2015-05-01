import subprocess
import sys
from platform.exception import WrongTargets
from platform.command import Command
from src.settings import Settings
from src.projects_repo import Repo
from commands.get import Get


def make(self, make_targets, name, makefile_path):
    prj = Repo.projects[name]
    sp = subprocess.Popen(['ssh', 'wmidevaddr', 'cd /home/massaraksh/ws; readlink -m .'], stdout=subprocess.PIPE)
    path = sp.stdout.readlines()[0].decode("utf-8").rstrip()
    jobs = 'CORENUM=$(cat /proc/cpuinfo | grep \"^processor\" | wc -l)'
    command = "cd {0}/{1}/{2}; {3}; make {4} -j$CORENUM 2>&1".format(prj['path'], name, makefile_path, jobs,
                                                                     ' '.join(make_targets))
    proc = subprocess.Popen(['ssh', prj['host'], command], stdout=subprocess.PIPE)
    while proc.poll() is None:
        line = proc.stdout.readline().decode("utf-8")
        line = line.replace(path, '/Users/massaraksh/ws')
        line = line.replace('/home/massaraksh/', '/Users/massaraksh/')
        sys.stderr.write(line)


class Make(Command):
    def help(self):
        print('rs make - вызывает Makefile на удалённой машине')
        print('rs make цели -- названия_проектов')
        print('rs make цели - название_проекта папка_с_Makefile')
        print('rs make --help')

    def check(self, p):
        if len(p.delimer) + len(p.doubleDelimer) != 1:
            print(str(p.delimer) + ' ' + str(p.doubleDelimer))
            raise WrongTargets('Неверное число разделителей: ' + str(p.argv))

        doubleDelimer = len(p.doubleDelimer) != 0
        sepIndex = p.doubleDelimer[0] if doubleDelimer else p.delimer[0]

        if sepIndex == 0:
            raise WrongTargets('отсутствуют цели Makefile' + str(p.argv))
        if sepIndex == len(p.argv) - 1:
            raise WrongTargets('отсутствуют проеты для сборки: ' + str(p.argv))

        projects = p.argv[sepIndex + 1:]

        if not doubleDelimer:
            if len(projects) != 2:
                raise WrongTargets(
                    'Слишком много параметров для сборки проекта с указанием пути до Makefile: ' + str(projects))
            if projects[0] not in Repo.projects:
                raise WrongTargets('Нет такого проекта: ' + projects[0])
        else:
            for proj in projects:
                if proj not in Repo.projects:
                    raise WrongTargets('Нет такого проекта: ' + proj)

    def syncIncludes(self, project):
        print('Синхронизирую заголовки...')
        get = Get()
        get.syncPath(Settings.EXCLUDE_FROM, '~/ws/include', '~/ws/include', 'wmidevaddr')

    def process(self, p):
        doubleDelimer = len(p.doubleDelimer) != 0
        sepIndex = p.doubleDelimer[0] if doubleDelimer else p.delimer[0]

        make_targets = p.argv[0:sepIndex]
        targets = p.argv[sepIndex + 1:]

        if doubleDelimer:
            for project in targets:
                print('Проект ' + project)
                make(make_targets, project, '')
                self.syncIncludes(project)
        else:
            print('Проект ' + targets[0])
            make(make_targets, targets[0], targets[1])
            self.syncIncludes(targets[0])


module_commands = {'make': Make}

