from src.sync import SyncData, callSync
from platform.exception import WrongOptions, WrongTargets
from platform.command import Command
from src.settings import Settings
from os.path import expanduser


class Send(Command):
    def help(self):
        print('rs send - отправляет файлы на удалённый сервер')
        print('rs send название_проекта')
        print('rs send --help')

    def check(self, p):
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, excludeFrom, path, remotePath, host):
        callSync([Settings.RS_ARGS, '--cvs-exclude', excludeFrom, expanduser(path + '/'), host + ':' + remotePath])

    def process(self, p):
        try:
            for arg in p.targets:
                sd = SyncData(arg)
                sd.show()
                self.syncPath(sd.exclude_from, sd.path, sd.path, sd.host)
        except KeyError:
            self.error('Нет такого проекта: ' + arg)


module_commands = {'send': Send}
