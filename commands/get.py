from src.sync import SyncData, callSync
from platform.exception import WrongTargets, WrongOptions
from platform.command import Command
from platform.delimer import checkNoDelimers
from src.settings import Settings
from os.path import expanduser


class Get(Command):
    def help(self):
        print('rs get - получает файлы с удалённого сервера')
        print('rs get название_проекта')
        print('rs get --help')

    def check(self, p):
        checkNoDelimers(p)
        if len(p.targets) == 0:
            raise WrongTargets('Неверное число целей: ' + str(p.targets))

        if len(p.options) != 0:
            raise WrongOptions('Странные аргументы: ' + str(p.options))

    def syncPath(self, excludeFrom, path, remotePath, host):
        callSync([Settings.RS_ARGS, '--cvs-exclude', excludeFrom, host + ':' + remotePath + '/', expanduser(path)])

    def process(self, p):
        try:
            for arg in p.targets:
                sd = SyncData(arg)
                sd.show()
                self.syncPath(sd.exclude_from, sd.path, sd.path, sd.host)
        except KeyError as arg:
            self.error('Нет такого проекта: ' + str(arg))


module_commands = {'get': Get}

