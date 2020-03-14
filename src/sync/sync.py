from os.path import isfile
from os.path import join, expanduser
from platform.color.color import colored, Color
from src.db.config import Config
from src.db.database import Database
from src.db.project import Project
from src.db.workspace import Workspace


class Sync(object):
    def __init__(self, database: Database, obj: Project, ws: Workspace, backend_class, dry=False, erase_missing=False, ):
        self.ws = ws
        config = database.config

        self.dry = dry
        self.path = join(ws.path, obj.path)
        self.remotePath = self.ws.host + ':' + join(self.ws.path, obj.path)
        self.exclude = self._getExcludeFile(obj.path, config)
        self.backend = backend_class(args=config.argSync, exclude=self.exclude,
                                     dry=self.dry, erase_missing=erase_missing)
        self.options = self.backend.options()

    def _getExcludeFile(self, path, cfg: Config):
        f = expanduser(join(path, cfg.excludeFileName))
        return f if isfile(f) else join(cfg.settings.CONFIG_DIR, cfg.excludeFileName)

    def get(self):
        self.backend.get(source=self.remotePath, destination=expanduser(self.path), ws=self.ws)
        return self

    def send(self):
        self.backend.send(source=expanduser(self.path), destination=self.remotePath, ws=self.ws)
        return self

    def print(self):
        print(self)
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
