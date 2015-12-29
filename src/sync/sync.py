from os.path import isfile
from os.path import join, expanduser
from platform.color.color import colored, Color
from src.db.config import Config
from src.db.database import Database
from src.db.project import Project
from src.sync.rsyncscp import RsyncSync


class Sync(object):
    def __init__(self, database: Database, object, dry = False, erase_missing = False):
        ws = database.workspaces()[object.workspace] if isinstance(object, Project) else object
        config = database.config

        self.dry = dry
        self.path = join(object.path, object.name)
        self.remotePath = ws.host + ':' + join(ws.src, object.name)
        self.exclude = self._getExcludeFile(object.path, object.name, config)
        self.backend = RsyncSync(config.argSync, self.exclude, self.dry, erase_missing)
        self.options = self.backend.options()

    def _getExcludeFile(self, path, name, cfg: Config):
        f = expanduser(join(path, name, cfg.excludeFileName))
        return f if isfile(f) else join(cfg.settings.CONFIG_DIR, cfg.excludeFileName)

    def get(self):
        self.backend.sync(self.remotePath, expanduser(self.path))
        return self

    def send(self):
        self.backend.sync(expanduser(self.path), self.remotePath)
        return self

    def print(self):
        print (self)
        print()
        return self

    def __str__(self):
        return '\n'.join(['Локальная папка: {path}',
                          'Удалённая папка: {remotePath}',
                          'Файл с исключениями: {exclude}',
                          'Тестовый прогон: {dry}',
                          'Опции синхронизации: {options}'])\
            .format(path=colored(self.path, Color.blue),
                    remotePath=colored(self.remotePath, Color.blue),
                    exclude=colored(self.exclude, Color.blue),
                    dry=colored('Да' if self.dry else 'Нет', Color.blue),
                    options=colored(self.options, Color.blue))
