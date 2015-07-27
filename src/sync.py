from os.path import isfile
import subprocess
from src.config import Config
from src.database import Database
from src.project import Project
from os.path import join, expanduser


class ScpSync(object):
    def __init__(self, args, exclude, dry):
        self._options = ['rsync'] + ['--cvs-exclude', '--exclude-from='+exclude] + args
        if dry:
            self._options.append('-n')


    def options(self):
        return self._options

    def sync(self, source, destination):
        subprocess.call(self._options + [source+'/', destination])


class Sync(object):
    def __init__(self, database: Database, config: Config, object, dry = False):
        ws = database.workspaces()[object.workspace] if isinstance(object, Project) else object

        self.dry = dry
        self.path = join(object.path, object.name)
        self.remotePath = ws.host + ':' + join(ws.src, object.name)
        self.exclude = self._getExcludeFile(object.path, config)
        self.backend = ScpSync(config.argSync, self.exclude, self.dry)
        self.options = self.backend.options()

    def _getExcludeFile(self, path, cfg: Config):
        f = expanduser(join(path, cfg.excludeFileName))
        return f if isfile(f) else join(cfg.settings.CONFIG_DIR, cfg.excludeFileName)

    def get(self):
        self.backend.sync(self.remotePath, expanduser(self.path))
        return self

    def send(self):
        self.backend.sync(expanduser(self.path), self.remotePath)
        return self

    def print(self):
        print (self)
        return self

    def __str__(self):
        return '\n'.join(['Локальная папка: {path}',
                          'Удалённая папка: {remotePath}',
                          'Файл с исключениями: {exclude}',
                          'Тестовый прогон: {dry}',
                          'Опции синхронизации: {options}'])\
            .format(**self.__dict__)
