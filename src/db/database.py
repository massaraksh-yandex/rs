from platform.db import database
from src.db.config import Config
from src.db.settings import Settings
from src.db.workspace import Workspace
from src.db.project import Project


class Database(database.Database):
    def __init__(self, config=Config()):
        super().__init__(config, Settings())

    def _getDirByType(self, t):
        if t == Project:
            return self.settings.REMOTES_DIR
        elif t == Workspace:
            return self.settings.WORKSPACES_DIR
        elif t == Config:
            return self.settings.CONFIG_DIR
        else:
            raise Exception('Неизвестный тип')

    def projects(self):
        return self.select('*', Project)

    def workspaces(self):
        return self.select('*', Workspace)


def initconfig():
    db = Database(Config({
        'defaultWorkspace': 'arcadia',
        'homeFolderName': '/home',
        'excludeFileName': 'rsignore',
        'argSync': ['-avcC', '--out-format=%f -- %b %o'],
        'default_local_path': 'arcadia'
    }))
    db.update(db.config)
